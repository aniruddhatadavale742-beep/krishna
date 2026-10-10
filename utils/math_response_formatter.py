import re


class MathResponseFormatter:
    """
    KRISHNA Mathematical Response Formatter.

    Converts common LaTeX mathematics into readable
    terminal-friendly mathematical notation.

    Examples:

        \\frac{1}{3}
            -> 1/3

        \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}
            -> (−b ± √(b²−4ac))/2a

        \\pi r^2
            -> πr²

        \\times
            -> ×

        \\sqrt{x}
            -> √x

        \\text{Base Area}
            -> Base Area

    IMPORTANT:
        This formatter only changes mathematical formatting.
        It does NOT modify programming code blocks.
    """

    # =========================================================
    # MAIN FORMAT FUNCTION
    # =========================================================

    def format(self, text):

        if not text:
            return text

        # -----------------------------------------------------
        # Protect code blocks
        # -----------------------------------------------------

        protected_blocks = []

        def protect_code(match):

            protected_blocks.append(
                match.group(0)
            )

            return (
                f"__KRISHNA_CODE_BLOCK_{len(protected_blocks) - 1}__"
            )

        text = re.sub(
            r"```[\s\S]*?```",
            protect_code,
            text
        )

        # -----------------------------------------------------
        # Protect inline code
        # -----------------------------------------------------

        inline_code = []

        def protect_inline(match):

            inline_code.append(
                match.group(0)
            )

            return (
                f"__KRISHNA_INLINE_CODE_{len(inline_code) - 1}__"
            )

        text = re.sub(
            r"`[^`\n]+`",
            protect_inline,
            text
        )

        # =====================================================
        # REMOVE DISPLAY MATH DELIMITERS
        # =====================================================

        text = text.replace(
            r"\[",
            ""
        )

        text = text.replace(
            r"\]",
            ""
        )

        text = text.replace(
            r"\(",
            ""
        )

        text = text.replace(
            r"\)",
            ""
        )

        text = text.replace(
            "$$",
            ""
        )

        # =====================================================
        # CONVERT LATEX FRACTIONS
        # =====================================================

        text = self.convert_latex_command(
            text,
            r"\frac",
            self.format_fraction
        )

        # =====================================================
        # CONVERT BINOMIAL
        # =====================================================

        text = self.convert_latex_command(
            text,
            r"\binom",
            self.format_binomial
        )

        # =====================================================
        # CONVERT SQUARE ROOTS
        # =====================================================

        text = self.convert_latex_command(
            text,
            r"\sqrt",
            self.format_sqrt
        )

        # =====================================================
        # CONVERT TEXT
        # =====================================================

        text = self.convert_latex_command(
            text,
            r"\text",
            self.format_text
        )

        # =====================================================
        # OTHER TEXT COMMANDS
        # =====================================================

        text = self.convert_latex_command(
            text,
            r"\mathrm",
            self.format_text
        )

        text = self.convert_latex_command(
            text,
            r"\mathbf",
            self.format_text
        )

        text = self.convert_latex_command(
            text,
            r"\operatorname",
            self.format_text
        )

        # =====================================================
        # LATEX SYMBOLS
        # =====================================================

        symbols = {

            # Arithmetic
            r"\times": "×",
            r"\cdot": "·",
            r"\div": "÷",
            r"\pm": "±",
            r"\mp": "∓",

            # Relations
            r"\leq": "≤",
            r"\le": "≤",
            r"\geq": "≥",
            r"\ge": "≥",
            r"\neq": "≠",
            r"\ne": "≠",
            r"\approx": "≈",
            r"\equiv": "≡",
            r"\propto": "∝",

            # Calculus
            r"\infty": "∞",
            r"\partial": "∂",
            r"\nabla": "∇",
            r"\int": "∫",
            r"\sum": "Σ",
            r"\prod": "Π",

            # Greek
            r"\alpha": "α",
            r"\beta": "β",
            r"\gamma": "γ",
            r"\delta": "δ",
            r"\epsilon": "ε",
            r"\varepsilon": "ε",
            r"\theta": "θ",
            r"\vartheta": "ϑ",
            r"\lambda": "λ",
            r"\mu": "μ",
            r"\pi": "π",
            r"\rho": "ρ",
            r"\sigma": "σ",
            r"\tau": "τ",
            r"\phi": "φ",
            r"\varphi": "φ",
            r"\omega": "ω",

            # Capital Greek
            r"\Gamma": "Γ",
            r"\Delta": "Δ",
            r"\Theta": "Θ",
            r"\Lambda": "Λ",
            r"\Sigma": "Σ",
            r"\Phi": "Φ",
            r"\Omega": "Ω",

            # Sets
            r"\in": "∈",
            r"\notin": "∉",
            r"\subset": "⊂",
            r"\subseteq": "⊆",
            r"\supset": "⊃",
            r"\supseteq": "⊇",
            r"\cup": "∪",
            r"\cap": "∩",
            r"\emptyset": "∅",

            # Logic
            r"\forall": "∀",
            r"\exists": "∃",
            r"\therefore": "∴",
            r"\because": "∵",

            # Misc
            r"\degree": "°",
            r"\circ": "∘",
            r"\ldots": "…",
            r"\dots": "…",
        }

        # Longer commands first.
        for old, new in sorted(
            symbols.items(),
            key=lambda item: len(item[0]),
            reverse=True
        ):

            text = text.replace(
                old,
                new
            )

        # =====================================================
        # LATEX SPACING COMMANDS
        # =====================================================

        text = text.replace(
            r"\quad",
            " "
        )

        text = text.replace(
            r"\qquad",
            " "
        )

        text = text.replace(
            r"\ ",
            " "
        )

        text = text.replace(
            r"\,",
            " "
        )

        text = text.replace(
            r"\;",
            " "
        )

        text = text.replace(
            r"\:",
            " "
        )

        text = text.replace(
            r"\!",
            ""
        )

        # =====================================================
        # SUPERSCRIPTS
        # =====================================================

        text = self.convert_superscripts(
            text
        )

        # =====================================================
        # SUBSCRIPTS
        # =====================================================

        text = self.convert_subscripts(
            text
        )

        # =====================================================
        # BASIC LATEX BRACES
        # =====================================================

        text = text.replace(
            "{",
            "("
        )

        text = text.replace(
            "}",
            ")"
        )

        # Fix simple cases created above.
        text = text.replace(
            "((",
            "("
        )

        text = text.replace(
            "))",
            ")"
        )

        # =====================================================
        # REMAINING LATEX COMMANDS
        # =====================================================

        # Only remove the backslash from unknown commands.
        # This prevents raw "\something" from remaining visible.
        text = re.sub(
            r"\\([a-zA-Z]+)",
            r"\1",
            text
        )

        # =====================================================
        # NORMAL MATHEMATICAL SYMBOLS
        # =====================================================

        text = text.replace(
            "<=",
            "≤"
        )

        text = text.replace(
            ">=",
            "≥"
        )

        text = text.replace(
            "!=",
            "≠"
        )

        text = text.replace(
            "->",
            "→"
        )

        text = text.replace(
            "<-",
            "←"
        )

        # =====================================================
        # MINUS SIGN
        # =====================================================

        text = text.replace(
            "-",
            "−"
        )

        # =====================================================
        # CLEAN SPACING
        # =====================================================

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        # Keep blank lines between paragraphs.
        text = re.sub(
            r"\n[ \t]+",
            "\n",
            text
        )

        # =====================================================
        # RESTORE INLINE CODE
        # =====================================================

        for index, code in enumerate(
            inline_code
        ):

            text = text.replace(
                f"__KRISHNA_INLINE_CODE_{index}__",
                code
            )

        # =====================================================
        # RESTORE CODE BLOCKS
        # =====================================================

        for index, code in enumerate(
            protected_blocks
        ):

            text = text.replace(
                f"__KRISHNA_CODE_BLOCK_{index}__",
                code
            )

        return text.strip()

    # =========================================================
    # LATEX COMMAND PARSER
    # =========================================================

    def convert_latex_command(
        self,
        text,
        command,
        formatter
    ):
        """
        Safely handles commands containing nested braces.

        Example:

            \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}

        The old regex could not handle this correctly.
        This parser can.
        """

        search_position = 0

        while True:

            position = text.find(
                command,
                search_position
            )

            if position == -1:
                break

            brace_start = position + len(
                command
            )

            # Skip whitespace.
            while (
                brace_start < len(text)
                and text[brace_start].isspace()
            ):

                brace_start += 1

            if (
                brace_start >= len(text)
                or text[brace_start] != "{"
            ):

                search_position = (
                    position + len(command)
                )

                continue

            first_content = self.extract_braced_content(
                text,
                brace_start
            )

            if first_content is None:

                search_position = (
                    position + len(command)
                )

                continue

            first_value, first_end = first_content

            # -------------------------------------------------
            # Commands needing two arguments
            # -------------------------------------------------

            if command in (
                r"\frac",
                r"\binom",
            ):

                second_start = first_end + 1

                while (
                    second_start < len(text)
                    and text[second_start].isspace()
                ):

                    second_start += 1

                if (
                    second_start >= len(text)
                    or text[second_start] != "{"
                ):

                    search_position = (
                        position + len(command)
                    )

                    continue

                second_content = self.extract_braced_content(
                    text,
                    second_start
                )

                if second_content is None:

                    search_position = (
                        position + len(command)
                    )

                    continue

                second_value, second_end = second_content

                replacement = formatter(
                    first_value,
                    second_value
                )

                text = (
                    text[:position]
                    + replacement
                    + text[second_end + 1:]
                )

                search_position = position

            else:

                replacement = formatter(
                    first_value
                )

                text = (
                    text[:position]
                    + replacement
                    + text[first_end + 1:]
                )

                search_position = position

        return text

    # =========================================================
    # EXTRACT BRACED CONTENT
    # =========================================================

    def extract_braced_content(
        self,
        text,
        opening_position
    ):
        """
        Extract content from {...}, including nested braces.
        """

        if (
            opening_position >= len(text)
            or text[opening_position] != "{"
        ):

            return None

        depth = 0

        for index in range(
            opening_position,
            len(text)
        ):

            character = text[index]

            if character == "{":

                depth += 1

            elif character == "}":

                depth -= 1

                if depth == 0:

                    content = text[
                        opening_position + 1:index
                    ]

                    return (
                        content,
                        index
                    )

        return None

    # =========================================================
    # FRACTION
    # =========================================================

    def format_fraction(
        self,
        numerator,
        denominator
    ):

        numerator = self.format(
            numerator
        )

        denominator = self.format(
            denominator
        )

        return (
            f"({numerator})/{denominator}"
        )

    # =========================================================
    # BINOMIAL
    # =========================================================

    def format_binomial(
        self,
        top,
        bottom
    ):

        top = self.format(
            top
        )

        bottom = self.format(
            bottom
        )

        return (
            f"C({top}, {bottom})"
        )

    # =========================================================
    # SQUARE ROOT
    # =========================================================

    def format_sqrt(
        self,
        content
    ):

        content = self.format(
            content
        )

        # Parentheses are useful for complex expressions.
        if (
            "+" in content
            or "−" in content
            or "×" in content
            or "/" in content
        ):

            return f"√({content})"

        return f"√{content}"

    # =========================================================
    # TEXT
    # =========================================================

    def format_text(
        self,
        content
    ):

        return self.format(
            content
        )

    # =========================================================
    # SUPERSCRIPT CONVERSION
    # =========================================================

    def convert_superscripts(
        self,
        text
    ):

        superscripts = {
            "0": "⁰",
            "1": "¹",
            "2": "²",
            "3": "³",
            "4": "⁴",
            "5": "⁵",
            "6": "⁶",
            "7": "⁷",
            "8": "⁸",
            "9": "⁹",
            "+": "⁺",
            "-": "⁻",
            "−": "⁻",
            "(": "⁽",
            ")": "⁾",
        }

        def convert(match):

            value = match.group(1)

            result = ""

            for character in value:

                result += superscripts.get(
                    character,
                    character
                )

            return result

        # x^{2} -> x²
        text = re.sub(
            r"\^\{([^{}]+)\}",
            convert,
            text
        )

        # x^2 -> x²
        text = re.sub(
            r"\^([0-9]+)",
            convert,
            text
        )

        return text

    # =========================================================
    # SUBSCRIPT CONVERSION
    # =========================================================

    def convert_subscripts(
        self,
        text
    ):

        subscripts = {
            "0": "₀",
            "1": "₁",
            "2": "₂",
            "3": "₃",
            "4": "₄",
            "5": "₅",
            "6": "₆",
            "7": "₇",
            "8": "₈",
            "9": "₉",
            "+": "₊",
            "-": "₋",
        }

        def convert(match):

            value = match.group(1)

            result = ""

            for character in value:

                result += subscripts.get(
                    character,
                    character
                )

            return result

        # x_{1} -> x₁
        text = re.sub(
            r"_\{([0-9+\-]+)\}",
            convert,
            text
        )

        # x_1 -> x₁
        text = re.sub(
            r"_([0-9]+)",
            convert,
            text
        )

        return text