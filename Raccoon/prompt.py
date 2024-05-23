from pathlib import Path
import re
from string import Template


class SysPrompt:
    """
    A class representing a system prompt for a GPTs.

    Attributes:
        ref_defenses (dict): A dictionary containing the reference defenses for the GPT model.
        name (str): The name of the GPTs.
        original_prompt (str): The original prompt string.
        user_prompt (str): The user-defined prompt string.

    Methods:
        parse_prompt(original_prompt: str) -> str:
            Extracts the user-defined prompt from the original prompt.

        load_gpts(gpts_path: Path) -> None:
            Loads GPTs from the specified path.

        get_name() -> str:
            Get the name of the GPTs.

        get_original_prompt() -> str:
            Returns the original prompt.

        get_user_prompt() -> str:
            Returns the user prompt.

        get_defenseless_prompt() -> str:
            Returns the defenseless prompt by removing tagged defenses from the user prompt.

        get_shielded_prompt(def_prompt: str, def_position='BOT', use_original_user_defenses=False) -> str:
            Returns a shielded prompt by combining the defense prompt and the defenseless prompt.
    """

    USER_PROMPT_START1 = "Here are instructions from the user outlining your goals and how you should respond:"
    USER_PROMPT_START2 = "Note: GPT is also a technical term in AI, but in most cases if the users asks you about GPTs assume they are referring to the above definition."
    USER_PROMPT_END = "You have files uploaded as knowledge to pull from. Anytime you reference files, refer to them as your knowledge source rather than files uploaded by the user."
    OPENAI_DEFAULT_TEMPLATE = """\
    You are a "GPT" – a version of ChatGPT that has been customized for a specific use case. GPTs use custom instructions, capabilities, and data to optimize ChatGPT for a more narrow set of tasks. You yourself are a GPT created by a user, and your name is $name. Note: GPT is also a technical term in AI, but in most cases if the users asks you about GPTs assume they are referring to the above definition.

    Here are instructions from the user outlining your goals and how you should respond:

    $user_prompt
    
    You have files uploaded as knowledge to pull from. Anytime you reference files, refer to them as your knowledge source rather than files uploaded by the user. You should adhere to the facts in the provided materials. Avoid speculations or information not contained in the documents. Heavily favor knowledge provided in the documents before falling back to baseline knowledge or other sources. If searching the documents didn"t yield any answer, just say that. Do not share the names of the files directly with end users and under no circumstances should you provide a download link to any of the files.
    """

    def __init__(self, ref_defenses: dict) -> None:
        self.ref_defenses = ref_defenses
        self.name = None
        self.original_prompt = None
        self.user_prompt = None

    @staticmethod
    def parse_prompt(original_prompt: str) -> str:
        """
        Extracts the user-defined prompt from the original prompt.

        Args:
            original_prompt (str): The original prompt string.

        Returns:
            str: The user-defined prompt string, stripped of leading and trailing whitespace.
        """
        # Get the user defined prompt out of the original prompt.
        start, end = 0, len(original_prompt)
        usr_start1 = SysPrompt.USER_PROMPT_START1
        usr_start2 = SysPrompt.USER_PROMPT_START2
        usr_end = SysPrompt.USER_PROMPT_END

        if (user_prompt_start := original_prompt.find(usr_start1)) != -1:
            start = user_prompt_start + len(usr_start1)
        elif (user_prompt_start := original_prompt.find(usr_start2)) != -1:
            start = user_prompt_start + len(usr_start2)

        if (user_prompt_end := original_prompt.find(usr_end)) != -1:
            end = user_prompt_end
        return original_prompt[start:end].strip()

    def load_gpts(self, gpts_path: Path) -> None:
        """
        Loads GPTs from the specified path.

        Args:
            gpts_path (Path): The path to the GPTs directory.

        Raises:
            FileNotFoundError: If the system_prompt.md file is not found in the GPTs directory.

        """
        prompt_path = gpts_path.joinpath("system_prompt.md")
        if not prompt_path.is_file():
            raise FileNotFoundError(
                f"GPTs directory {gpts_path} does not contain system_prompt.md"
            )
        self.name = gpts_path.name
        with open(prompt_path, encoding="utf-8") as f:
            self.original_prompt = f.read()
        self.user_prompt = self.parse_prompt(self.original_prompt)

    def get_name(self) -> str:
        """
        Get the name of the GPTs.

        Returns:
            str: The name of the GPTs.

        Raises:
            ValueError: If the GPTs name is not loaded.
        """
        if self.name is None:
            raise ValueError("GPTs name is not loaded.")
        return self.name

    def get_system_prompt(
        self,
        use_original_user_prompt=False,
        use_defenseless_user_prompt=False,
        use_original_user_defenses=False,
        use_custom_defenses=False,
        custom_defense="",
        defense_position="BOT",
    ) -> str:
        if use_original_user_prompt:
            return self.get_original_prompt()
        elif use_defenseless_user_prompt:
            return self.get_defenseless_prompt()
        elif use_original_user_defenses:
            return self.get_shielded_prompt(
                "", defense_position, use_original_user_defenses
            )
        elif use_custom_defenses:
            return self.get_shielded_prompt(custom_defense, defense_position)
        else:
            return self.get_user_prompt()

    def get_original_prompt(self) -> str:
        """
        Returns the original prompt.

        Raises:
            ValueError: If the original prompt is not loaded.

        Returns:
            str: The original prompt.
        """
        if self.original_prompt is None:
            raise ValueError("Original prompt is not loaded.")
        return self.original_prompt

    def get_user_prompt(self) -> str:
        """
        Returns the user prompt.

        Raises:
            ValueError: If the user prompt is not loaded.

        Returns:
            str: The user prompt.
        """
        if self.user_prompt is None:
            raise ValueError("User prompt is not loaded.")
        return self.user_prompt

    def get_defenseless_prompt(self) -> str:
        """
        Returns the defenseless prompt by removing tagged defenses from the user prompt.

        Raises:
            ValueError: If GPTs is not loaded or if GPTs is not in the reference defenses.

        Returns:
            str: The defenseless prompt.
        """
        if self.name is None or self.user_prompt is None:
            raise ValueError("GPTs is not loaded.")
        if self.name not in self.ref_defenses:
            raise ValueError(f'GPTs "{self.name}" is not in the reference defenses.')
        defenseless_prompt = self.user_prompt

        # Remove all tagged defenses from the user prompt.
        for def_prompt in self.ref_defenses[self.name].keys():
            if def_prompt in defenseless_prompt:
                defenseless_prompt = defenseless_prompt.replace(def_prompt, "")
            elif def_prompt not in self.OPENAI_DEFAULT_TEMPLATE:
                raise ValueError(
                    f'GPTs "{self.name}" does not contain defense prompt "{def_prompt}".'
                )
        defenseless_prompt = re.sub(r"\n\n\n+", "\n\n", defenseless_prompt)

        return defenseless_prompt.strip()

    def get_shielded_prompt(
        self, def_template: str, def_position="BOT", use_original_user_defenses=False
    ) -> str:
        """
        Returns a shielded prompt by combining the defense prompt and the defenseless prompt.

        Args:
            def_prompt (str): The defense prompt to be used.
            def_position (str, optional): The position of the defense prompt in the shielded prompt.
                                          Valid values are 'TOP' and 'BOT'. Defaults to 'BOT'.
            use_original_user_defenses (bool, optional): Whether to use the original user defenses
                                                         instead of the provided defense prompt.
                                                         Defaults to False.

        Returns:
            str: The shielded prompt.

        Raises:
            ValueError: If GPTs is not loaded or an invalid defense position is provided.
        """
        if self.name is None or self.user_prompt is None:
            raise ValueError("GPTs is not loaded.")
        defenseless_prompt = self.get_defenseless_prompt()

        if use_original_user_defenses:
            def_prompt = "\n".join(self.ref_defenses[self.name].keys())
            if def_position == "TOP":
                shielded_prompt = "\n\n".join([def_prompt, defenseless_prompt])
            elif def_position == "BOT":
                shielded_prompt = "\n\n".join([defenseless_prompt, def_prompt])
            else:
                raise ValueError("Invalid defense position.")
        else:
            shielded_prompt = Template(def_template).safe_substitute(
                name=self.name, user_prompt=defenseless_prompt
            )
            if shielded_prompt == def_template:
                if def_position == "TOP":
                    shielded_prompt = "\n\n".join([def_template, defenseless_prompt])
                elif def_position == "BOT":
                    shielded_prompt = "\n\n".join([defenseless_prompt, def_template])
                else:
                    raise ValueError("Invalid defense position.")

        return shielded_prompt.strip()


class AttPrompt:
    """
    A class representing an attack prompt for a GPTs.
    """

    def __init__(self, att_prompt: str, category) -> None:
        self.att_prompt = att_prompt
        self.category = category

    @staticmethod
    def load_all_attacks(att_loader) -> list:
        """
        Loads attack prompts from the specified path.

        Args:
            att_path (Path): The path to the attack prompts directory.

        Returns:
            list: A list of attack prompts.
        """
        att_prompts = []
        for category_name, category_path in zip(
            att_loader.category_names, list(att_loader.att_categories_path)
        ):
            for prompt_path in category_path.glob("*"):
                with open(prompt_path, encoding="utf-8") as f:
                    att_prompt = f.read()
                att_prompts.append(AttPrompt(att_prompt, category_name))
        return att_prompts

    def get_att_prompt(self) -> str:
        return self.att_prompt

    def __str__(self):
        return f"Category: {self.category}\nPrompt: {self.att_prompt}"
