from azul_runner import FV, Event, JobResult, State, test_template

from azul_plugin_alphabets.main import AzulPluginAlphabets

EXAMPLE_32 = b"abcdefghijklmnopqrstuvwxyz123456"
EXAMPLE_64 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
CUSTOM_64 = b"ABCDEJKLMFGHINOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


class TestAlphabets(test_template.TestPlugin):
    PLUGIN_TO_TEST = AzulPluginAlphabets

    def test_no_matches(self):
        """No features expected"""
        result = self.do_execution(data_in=[("content", b"abbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcd")])
        self.assertJobResult(result, JobResult(state=State(State.Label.COMPLETED_EMPTY)))

    def test_b64_alphabet(self):
        """Single base64 alphabet expected"""
        content = b"\x00\x01\x02AA\n" + EXAMPLE_64 + b"\nSomething"
        result = self.do_execution(data_in=[("content", content)])
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="d9a439d09551b62af7c289a39a8c26f7e85f510cf8232546150b99258b2263b1",
                        features={
                            "b64_alphabet": [
                                FV(
                                    value=EXAMPLE_64.decode(),
                                    offset=content.find(EXAMPLE_64),
                                    size=len(EXAMPLE_64.decode()),
                                )
                            ],
                            "b64_alphabet_count": [FV(1)],
                        },
                    )
                ],
            ),
        )

    def test_multiple_alphabets(self):
        """Multiple alphabets and counts expected"""
        content = b"\x00" + EXAMPLE_32 + b"\x00\x02\x00" + CUSTOM_64 + b"\x00" + EXAMPLE_64
        result = self.do_execution(
            data_in=[
                (
                    "content",
                    content,
                )
            ]
        )
        self.assertJobResult(
            result,
            JobResult(
                state=State(State.Label.COMPLETED),
                events=[
                    Event(
                        sha256="9b553d89abf7aa93fad2c82546549e467cf8a954397ab9c2837d89df914dad7c",
                        features={
                            "b32_alphabet": [
                                FV(
                                    value=EXAMPLE_32.decode(),
                                    offset=content.find(EXAMPLE_32),
                                    size=len(EXAMPLE_32.decode()),
                                )
                            ],
                            "b32_alphabet_count": [FV(1)],
                            "b64_alphabet": [
                                FV(
                                    value=EXAMPLE_64.decode(),
                                    offset=content.find(EXAMPLE_64),
                                    size=len(EXAMPLE_64.decode()),
                                ),
                                FV(
                                    value=CUSTOM_64.decode(),
                                    offset=content.find(CUSTOM_64),
                                    size=len(CUSTOM_64.decode()),
                                ),
                            ],
                            "b64_alphabet_count": [FV(2)],
                        },
                    )
                ],
            ),
        )
