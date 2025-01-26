from typing import Callable, List, Literal, Optional

from pydantic import BaseModel

DAISY_UI_THEMES = Literal[
    "light",
    "dark",
    "cupcake",
    "bumblebee",
    "emerald",
    "corporate",
    "synthwave",
    "retro",
    "cyberpunk",
    "valentine",
    "halloween",
    "garden",
    "forest",
    "aqua",
    "lofi",
    "pastel",
    "fantasy",
    "wireframe",
    "black",
    "luxury",
    "dracula",
    "cmyk",
    "autumn",
    "business",
    "acid",
    "lemonade",
    "night",
    "coffee",
    "winter",
    "dim",
    "nord",
    "sunset",
]


class PipelineConfig(BaseModel):
    title: str
    function: Callable
    disclaimer: Optional[str] = None
    info: Optional[str] = None
    sample_questions: List[str] = None
    theme: DAISY_UI_THEMES = "dark"


class RagUI:
    def __init__(self):
        self._pipelines = {}

    def pipeline(
        self,
        *,
        title: str,
        disclaimer: Optional[str] = None,
        info: Optional[str] = None,
        sample_questions: List[str] = None,
        theme: DAISY_UI_THEMES = Literal["dark"],
    ):
        def decorator(func):
            self._pipelines[func.__name__] = PipelineConfig(
                title=title,
                function=func,
                disclaimer=disclaimer,
                info=info,
                sample_questions=sample_questions,
                theme=theme,
            )
            return func

        return decorator

    @property
    def pipelines(self):
        return self._pipelines
