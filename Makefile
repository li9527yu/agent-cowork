.PHONY: check smoke-test demo clean-demo

check:
	python3 tools/agent-context.py status

smoke-test:
	./scripts/smoke-test.sh

demo:
	python3 tools/agent-context.py scaffold DEMO-001 --title "Demo task" --owner "demo" --source "local demo"
	python3 tools/agent-context.py check DEMO-001

clean-demo:
	rm -rf docs/tasks/DEMO-001
