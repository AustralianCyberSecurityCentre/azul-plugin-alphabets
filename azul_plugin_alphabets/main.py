"""Find character runs consistent with possible encoding schemes (base64, etc).

It does not perform any decoding, just identification of the possible alphabets/usage.
The plugin supports the following encoding schemes:
    * base32
    * base64
    * base85
"""

from azul_runner import BinaryPlugin, Feature, Job, cmdline_run

from . import b64_alphabet_finder


class AzulPluginAlphabets(BinaryPlugin):
    """Find character runs consistent with possible encoding schemes (base64, etc)."""

    CONTACT = "ASD's ACSC"
    VERSION = "2025.12.10"
    FEATURES = [
        Feature(name="b32_alphabet", desc="Possible base32 alphabet", type=str),
        Feature(name="b32_alphabet_count", desc="Count of possible base32 alphabets", type=int),
        Feature(name="b64_alphabet", desc="Possible base64 alphabet", type=str),
        Feature(name="b64_alphabet_count", desc="Count of possible base64 alphabets", type=int),
        Feature(name="b85_alphabet", desc="Possible base85 alphabet", type=str),
        Feature(name="b85_alphabet_count", desc="Count of possible base85 alphabets", type=int),
    ]
    SECURITY = "MORE OFFICIAL REL:APPLE,DOG"

    def filter_lengths(self, lengths, strings):
        """Filter the list of strings based on their length."""
        return [x for x in strings if len(x) in lengths]

    def execute(self, job: Job):
        """Search for alphabets in the supplied entity's content."""
        features = {}
        res = b64_alphabet_finder.find_basen_alphabets(job.get_data().read())
        if res:
            features["b32_alphabet"] = self.filter_lengths([32], res)
            features["b64_alphabet"] = self.filter_lengths([64, 65], res)
            features["b85_alphabet"] = self.filter_lengths([85], res)
            if len(features["b32_alphabet"]):
                features["b32_alphabet_count"] = len(features["b32_alphabet"])
            if len(features["b64_alphabet"]):
                features["b64_alphabet_count"] = len(features["b64_alphabet"])
            if len(features["b85_alphabet"]):
                features["b85_alphabet_count"] = len(features["b85_alphabet"])
            self.add_many_feature_values(features)


def main():
    """Command-line entrypoint to start the plugin."""
    cmdline_run(plugin=AzulPluginAlphabets)


if __name__ == "__main__":
    main()
