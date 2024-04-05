import pymsteams

from config.config import WEB_HOOK

team_message = pymsteams.connectorcard(WEB_HOOK)
with open("reports/markdown/report.md") as report:
    report_message = report.read()

print(report_message)
# team_message.text(report_message)
# team_message.send()
