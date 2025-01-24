from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Static
from art import text2art

class CategoryTitle(Static):
    pass

class ValueButton(Button):
    pass

class JeopardyBanner(Static):
    pass

class TeamScore(Static):
    def __init__(self, team_name: str, initial_score: int = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.team_name = text2art(team_name, font="bulbhead")
        self.score = initial_score
        self.update(self._formatted_score)
    
    @property
    def _formatted_score(self) -> str:
        return f"{self.team_name}\n[bold #ffff00]${self.score}[/]"

class JeopardyApp(App):
    CSS_PATH = "jeopardy.tcss"
    
    CATEGORIES = [
        "The American\nRevolution",
        "Waikiki's\nLandmarks", 
        "Gourmet\nCuisine",
        "Professional\nChess 'A'",
        "1990's\nMovies",
        "The Animal\nKingdom"
    ]
    
    QUESTIONS_PER_CATEGORY = 5
    BASE_VALUE = 200
    TEAM_COUNT = 5
    BANNER_ART = r"""
     _      __  __      _
    / \    |  \/  |    / \
   / _ \   | |\/| |   / _ \
  / ___ \ _| |  | |_ / ___ \
 /_/   \_(_)_|  |_(_)_/   \_\
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Grid():
                yield from (CategoryTitle(category) for category in self.CATEGORIES)
                for row in range(self.QUESTIONS_PER_CATEGORY):
                    value = self.BASE_VALUE * (row + 1)
                    yield from (ValueButton(f"${value}") for _ in self.CATEGORIES)
            
            with VerticalScroll(classes="sidebar"):
                yield JeopardyBanner(self.BANNER_ART)
                for team_id in range(self.TEAM_COUNT):
                    yield TeamScore(
                        f"T{team_id+1}", 
                        0, 
                        classes=f"score-box team-{team_id+1}"
                    )

    def on_mount(self) -> None:
        self.title = "AMA"

if __name__ == "__main__":
    JeopardyApp().run()
