from authomatic.exceptions import FetchError
from authomatic.providers import BaseProvider
from http import client as http_client
from pas.plugins.authomatic.logging import logger
from urllib import parse

import authomatic.core
import ssl


def patch_base_provider_fetch():
    def _fetch(
        self,
        url,
        method="GET",
        params=None,
        headers=None,
        body="",
        max_redirects=5,
        content_parser=None,
        certificate_file=None,
        ssl_verify=True,
    ):
        """
        Fetches a URL.

        :param str url:
            The URL to fetch.

        :param str method:
            HTTP method of the request.

        :param dict params:
            Dictionary of request parameters.

        :param dict headers:
            HTTP headers of the request.

        :param str body:
            Body of ``POST``, ``PUT`` and ``PATCH`` requests.

        :param int max_redirects:
            Number of maximum HTTP redirects to follow.

        :param function content_parser:
            A callable to be used to parse the :attr:`.Response.data`
            from :attr:`.Response.content`.

        :param str certificate_file:
            Optional certificate file to be used for HTTPS connection.

        :param bool ssl_verify:
            Verify SSL on HTTPS connection.
        """
        # 'magic' using _kwarg method
        # pylint:disable=no-member
        params = params or {}
        params.update(self.access_params)

        headers = headers or {}
        headers.update(self.access_headers)

        url_parsed = parse.urlsplit(url)
        query = parse.urlencode(params)

        if method in ("POST", "PUT", "PATCH"):
            if not body:
                # Put querystring to body
                body = query
                query = ""
                headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        request_path = parse.urlunsplit(
            ("", "", url_parsed.path or "", query or "", "")
        )

        self._log_param("host", url_parsed.hostname, last=False)
        self._log_param("method", method, last=False)
        self._log_param("body", body, last=False)
        self._log_param("params", params, last=False)
        self._log_param("headers", headers, last=False)
        self._log_param("certificate", certificate_file, last=False)
        self._log_param("SSL verify", ssl_verify, last=True)

        # Connect
        if url_parsed.scheme.lower() == "https":
            if ssl_verify:
                context = ssl.create_default_context(
                    purpose=ssl.Purpose.SERVER_AUTH, cafile=certificate_file
                )
            else:
                context = ssl._create_unverified_context()

            connection = http_client.HTTPSConnection(
                url_parsed.hostname, port=url_parsed.port, context=context
            )
        else:
            connection = http_client.HTTPConnection(
                url_parsed.hostname, port=url_parsed.port
            )

        try:
            connection.request(method, request_path, body, headers)
        except Exception as e:  # noQA: B902
            raise FetchError(
                "Fetching URL failed", original_message=str(e), url=request_path
            )

        response = connection.getresponse()
        location = response.getheader("Location")

        if response.status in (300, 301, 302, 303, 307) and location:
            if location == url:
                raise FetchError(
                    "Url redirects to itself!", url=location, status=response.status
                )

            if max_redirects > 0:
                remaining_redirects = max_redirects - 1

                self._log_param("Redirecting to", url)
                self._log_param("Remaining redirects", remaining_redirects)

                # Call this method again.
                response = self._fetch(
                    url=location,
                    params=params,
                    method=method,
                    headers=headers,
                    max_redirects=remaining_redirects,
                    certificate_file=certificate_file,
                    ssl_verify=ssl_verify,
                )

            else:
                raise FetchError(
                    "Max redirects reached!", url=location, status=response.status
                )
        else:
            self._log_param("Got response")
            self._log_param("url", url, last=False)
            self._log_param("status", response.status, last=False)
            self._log_param("headers", response.getheaders(), last=True)

        return authomatic.core.Response(response, content_parser)

    BaseProvider._fetch = _fetch
    logger.info("Patched authomatic.providers.BaseProvider._fetch")
