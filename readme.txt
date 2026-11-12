测试：python3 -m unittest discover -s tests/wakeup_delivery -p 'test_*.py'
构建：python3 -m compileall -q four_level_wakeup_hub tests/wakeup_delivery
验收：python3 -m four_level_wakeup_hub.dispatch.cli fixtures/demo.json --database /tmp/four_level_wakeup_hub-acceptance.sqlite3
