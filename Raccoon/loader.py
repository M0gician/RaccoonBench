from pathlib import Path


class Loader:
    """
    A class that represents a loader for OpenAI's GPTs.

    Args:
        gpts_dir (str): The directory path where the GPTs are located.

    Attributes:
        gpts (generator): A generator that yields the paths of the GPT files in the specified directory.
        gpts_iter (iterator): An iterator used to iterate over the GPT paths.

    """

    def __init__(self, gpts_dir: str) -> None:
        self.gpts = Path(gpts_dir).glob("*")
        self.gpts_iter = iter(self.gpts)

    def __iter__(self):
        return self

    def __next__(self):
        cur_gpts = next(self.gpts_iter)
        return cur_gpts

class AttLoader:
    def __init__(self, att_dir: str) -> None:
        self.att_categories_path = list(Path(att_dir).glob("*"))
        self.category_names = [category_path.name for category_path in self.att_categories_path]

        self.prompt_paths = {}
        for category_name, category_path in zip(self.category_names,list(self.att_categories_path)):
            self.prompt_paths[category_name] = list(category_path.glob("*"))
