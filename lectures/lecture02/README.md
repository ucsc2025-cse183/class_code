# URL - Universal Resource Locator

http://127.0.0.1:80/hello/world?a=1&b=2#xyz

====
http called the schema (http, https, ftp, ...)
       
       =========
       127.0.0.1 is address or hostname

                ===
                :80 port a number between 1 and 32,000

                   ============
                   /hello/world any string (PATH_INFO)

                               ========
                               ?a=1&b=2  (QUERY_STRING)

                                       =====
                                       #xyz (anchor)


request stars with "GET path_info?query string HTTP/1.1"

method GET
protocol HTTP/1.1
path_info /hello/world
query_string a=1&b=2

response starts with "HTTP/1.1 200 OK"

https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


                               


