import logging
import os

logger = logging.getLogger("django")

ragui = None


def init_ragui():
    global ragui
    script_path = os.getenv("RAGUI_SCRIPT")
    if not script_path:
        raise RuntimeError("RAGUI_SCRIPT environment variable not set")

    namespace = {}
    with open(script_path) as f:
        exec(f.read(), namespace)

    if "ragui" not in namespace:
        raise RuntimeError("No RagUI instance found in script")

    ragui = namespace["ragui"]
    logger.info("Loaded RagUI instance from %s", script_path)


def get_ragui_instance():
    if ragui is None:
        init_ragui()
    return ragui
