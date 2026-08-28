import tempfile
import unittest
from pathlib import Path

from validate_artifact import SUPPORTED_MERMAID_HEADERS, audit


VALID_ARTIFACT = """<!doctype html>
<html lang="en">
<head>
  <title>Request flow</title>
  <style>
    :root { --fs-micro: 16px; --fs-body: 18px; }
    body { font-size: var(--fs-body); }
    pre { font-family: var(--mono); font-weight: 400; }
    .js-mermaid.is-rendered > .diagram-source { display: none; }
  </style>
</head>
<body>
  <div class="js-mermaid" data-mermaid-max-scale="1.35" data-mermaid-min-text-token="--fs-micro">
    <pre class="diagram-source">flowchart LR; A --> B</pre>
    <div class="diagram-output"></div>
  </div>
  <script type="module">
    async function render() {
      const wrappers = document.querySelectorAll(".js-mermaid");
      if (!wrappers.length) return;
      await import("https://example.test/beautiful-mermaid.js");
    }
    render();
  </script>
</body>
</html>
"""


class ArtifactAuditTest(unittest.TestCase):
    def audit_source(self, source):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact.html"
            path.write_text(source, encoding="utf-8")
            return audit(path)

    def assert_rejected(self, replacement, expected):
        errors = self.audit_source(VALID_ARTIFACT.replace(*replacement))
        self.assertTrue(
            any(expected in error for error in errors),
            f"expected {expected!r} in {errors!r}",
        )

    def test_accepts_valid_fallback_first_artifact(self):
        self.assertEqual(self.audit_source(VALID_ARTIFACT), [])

    def test_rejects_font_token_below_minimum(self):
        self.assert_rejected(("--fs-body: 18px", "--fs-body: 15px"), "below 16px")

    def test_rejects_non_token_font_size(self):
        self.assert_rejected(("var(--fs-body)", ".5rem"), "must use a --fs-* token")

    def test_rejects_nonstandard_font_weight(self):
        self.assert_rejected(
            ("font-weight: 400", "font-weight: 720"),
            "must use 400, 500, 600, or 700",
        )

    def test_accepts_supported_font_weight_with_important(self):
        source = VALID_ARTIFACT.replace("font-weight: 400", "font-weight: 400 !important")
        self.assertEqual(self.audit_source(source), [])

    def test_rejects_mono_for_non_code_text(self):
        self.assert_rejected(
            (
                "body { font-size: var(--fs-body); }",
                "body { font-size: var(--fs-body); font-family: var(--mono); }",
            ),
            "reserve --mono for code",
        )

    def test_rejects_mermaid_without_maximum_scale(self):
        self.assert_rejected(
            (' data-mermaid-max-scale="1.35"', ""),
            "data-mermaid-max-scale",
        )

    def test_rejects_mermaid_without_minimum_text_token(self):
        self.assert_rejected(
            (' data-mermaid-min-text-token="--fs-micro"', ""),
            "minimum text token",
        )

    def test_rejects_unsupported_mermaid_diagram_type(self):
        self.assert_rejected(
            ("flowchart LR; A --> B", "pie title Share"),
            "unsupported diagram type 'pie'",
        )

    def test_accepts_every_supported_mermaid_diagram_type(self):
        for header in SUPPORTED_MERMAID_HEADERS:
            with self.subTest(header=header):
                source = VALID_ARTIFACT.replace("flowchart LR", f"{header} LR")
                self.assertEqual(self.audit_source(source), [])

    def test_rejects_direct_maple_font_on_non_code_text(self):
        self.assert_rejected(
            (
                "body { font-size: var(--fs-body); }",
                'body { font-size: var(--fs-body); font-family: "Maple Mono NF CN"; }',
            ),
            "reserve --mono for code",
        )

    def test_rejects_maple_assigned_to_sans_token(self):
        self.assert_rejected(
            (
                ":root { --fs-micro: 16px; --fs-body: 18px; }",
                ':root { --fs-micro: 16px; --fs-body: 18px; --sans: "Maple Mono NF CN"; }',
            ),
            "define Maple Mono only in --mono",
        )

    def test_rejects_mono_aliased_through_another_token(self):
        self.assert_rejected(
            (
                ":root { --fs-micro: 16px; --fs-body: 18px; }",
                ":root { --fs-micro: 16px; --fs-body: 18px; --body-font: var(--mono); }",
            ),
            "define Maple Mono only in --mono",
        )

    def test_rejects_direct_maple_font_shorthand_on_non_code_text(self):
        self.assert_rejected(
            (
                "body { font-size: var(--fs-body); }",
                'body { font-size: var(--fs-body); font: 400 var(--fs-body) "Maple Mono NF CN"; }',
            ),
            "reserve --mono for code",
        )

    def test_rejects_mono_font_shorthand_on_non_code_text(self):
        self.assert_rejected(
            (
                "body { font-size: var(--fs-body); }",
                "body { font-size: var(--fs-body); font: var(--mono); }",
            ),
            "reserve --mono for code",
        )

    def test_rejects_mono_on_selector_that_only_contains_code_substring(self):
        self.assert_rejected(
            (
                "body { font-size: var(--fs-body); }",
                ".decode-label { font-family: var(--mono); }",
            ),
            "reserve --mono for code",
        )

    def test_rejects_inline_font_shorthand(self):
        self.assert_rejected(("<body>", '<body style="font: 12px sans-serif">'), "inline font")

    def test_rejects_hidden_source_attribute(self):
        self.assert_rejected(
            ('class="diagram-source"', 'class="diagram-source" hidden'),
            "hides its source fallback",
        )

    def test_rejects_inline_hidden_source(self):
        self.assert_rejected(
            ('class="diagram-source"', 'class="diagram-source" style="display:none"'),
            "hides its source fallback",
        )

    def test_rejects_unconditional_css_hiding(self):
        self.assert_rejected(
            (".js-mermaid.is-rendered > .diagram-source", ".diagram-source"),
            "hidden only under an .is-rendered selector",
        )

    def test_rejects_mixed_selector_hiding(self):
        self.assert_rejected(
            (
                ".js-mermaid.is-rendered > .diagram-source",
                ".js-mermaid.is-rendered > .diagram-source, .diagram-source",
            ),
            "hidden only under an .is-rendered selector",
        )

    def test_rejects_hidden_renderer_wrapper(self):
        self.assert_rejected(
            (
                ".js-mermaid.is-rendered > .diagram-source { display: none; }",
                ".js-mermaid.is-rendered > .diagram-source { display: none; }\n.js-mermaid { display: none; }",
            ),
            "do not hide optional-renderer wrappers",
        )

    def test_rejects_top_level_dynamic_import(self):
        self.assert_rejected(
            ("async function render() {", 'await import("https://example.test/shiki.js");\nasync function render() {'),
            "inside a renderer",
        )

    def test_rejects_top_level_dynamic_import_in_classic_script(self):
        source = VALID_ARTIFACT.replace('type="module"', "").replace(
            "async function render() {",
            'await import("https://example.test/shiki.js");\nasync function render() {',
        )
        errors = self.audit_source(source)
        self.assertTrue(any("inside a renderer" in error for error in errors), errors)

    def test_rejects_unchanged_starter_marker(self):
        self.assert_rejected(
            ("<body>", "<body data-visual-explainer-starter>"),
            "replace template placeholders",
        )

    def test_rejects_template_with_only_sentinels_removed(self):
        template = Path(__file__).parents[1] / "assets" / "template.html"
        source = template.read_text(encoding="utf-8").replace('lang="und"', 'lang="en"')
        source = source.replace(" data-visual-explainer-starter", "")
        errors = self.audit_source(source)
        self.assertTrue(any("replace template placeholder" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
