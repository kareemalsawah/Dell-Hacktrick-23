text = "eyJraWQiOiI5MmM1YTU1MS0yNjFlLTQ5OTktOGQyMy0wMjM1YTg2NTM1NjEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp3ayI6eyJrdHkiOiJSU0EiLCJlIjoiQVFBQiIsImtpZCI6IjkyYzVhNTUxLTI2MWUtNDk5OS04ZDIzLTAyMzVhODY1MzU2MSIsIm4iOiJwZjdrQ19uVjgzZU1wZ3k2Mk81Nl9vVDIyd2FaVkZOMWhwU1FsYlpaWmJPNmQ0UUFQV1dJWDZTWXlaMUNqUWotSHVSTW1ndHJ4QWFiUmVJelpZaGFvUlV5WjMyR1FyY2lNMVFXb0hRSjJsV2dmVkNMX0Fhb2ZWaFlCbVVqVUFWcHRqMWdmSC1QQlYyYjdDOFNjTlhMWTI5cWVtV29qOS1icVpka3pvdHEzWGlaMU1NMUlfbXctOFBqSGg3TGpSaGM4WVJSb1I5UXhlOFpBQlRmUUNreGhxM1ZHYS14VkJlMFhyT1lTWGlfWHBMQV9SRXRuSjZmSXk1YlllQVYyTjVuWHFyOVFGQTkxVDVnUkR6VU1PNTFjRm42VUtHbnRJMTlxNDRKam91clVOYUw2Qlk5SU5LSjV5enBCRWlydWhzZGlLWDRxaFZyWVlPSllpTGNZSDJOd3cifX0.eyJpc3MiOiJodHRwczovL3NlcnZpY2VBLmVudjo4MDgwIiwiYXVkIjoiYWNjb3VudCIsImlkIjoiNTAxYTFiZjQtYjUyMy00OTNjLWI0NTctYWVmOTM1YTI0MWJhIiwic2NvcGUiOiJwcm9maWxlIiwibmFtZSI6IkJvYiBNYXJsZXkiLCJlbWFpbCI6ImJvYi5tYXJsZXlAaGFja3RyaWNrLmNvbSIsImFkbWluIjoiZmFsc2UiLCJyYW5kIjoiNSJ9.S0KACssre_Szq9zy02Rqb-mDBi0r5kNktMQmgZTnsZ-VOSkcRWeIX-grf_g_y7XFFQKH_g2wDjTitDXbRIHMgYx7rOkLtlHOULH84Tuu8bLM67YQqyfyuE-eKifO9RTWMpdOb0FY8IxscfXxq3qnXsW8wtmirufeLyZ4XKcLbazV9P5S3uKRi5mJwo0pUAmYKTv4xFh_bu9xCKluPMn3hijBZANMSmYeuvaaVWqStBo0sTwGN3rfcSofANL9nMpSZn2dD0iFQLTVCEVlWe8MGlrT6sBi9pSIQpi2zfnMKxV-B30xeOeKan_fC5Nm4yV6NMFQSzqRWlyKU_UqeDoemQ"
from riddle_solvers import *

ans = server_solver(text)
import base64

# print(ans)
ans = base64.b64decode(ans.split(".")[0] + "=" * (-len(ans) % 4))
print(ans)
