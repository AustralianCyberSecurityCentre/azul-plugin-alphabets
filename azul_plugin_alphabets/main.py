"""Find character runs consistent with possible encoding schemes (base64, etc).

It does not perform any decoding, just identification of the possible alphabets/usage.
The plugin supports the following encoding schemes:
    * base32
    * base64
    * base85
"""

from azul_runner import FV, BinaryPlugin, Feature, FeatureType, Job, cmdline_run

from . import b64_alphabet_finder


class AzulPluginAlphabets(BinaryPlugin):
    """Find character runs consistent with possible encoding schemes (base64, etc)."""

    CONTACT = "ASD's ACSC"
    VERSION = "2024.04.29"
    FEATURES = [
        Feature(name="b32_alphabet", desc="Possible base32 alphabet", type=FeatureType.String),
        Feature(name="b32_alphabet_count", desc="Count of possible base32 alphabets", type=FeatureType.Integer),
        Feature(name="b64_alphabet", desc="Possible base64 alphabet", type=FeatureType.String),
        Feature(name="b64_alphabet_count", desc="Count of possible base64 alphabets", type=FeatureType.Integer),
        Feature(name="b85_alphabet", desc="Possible base85 alphabet", type=FeatureType.String),
        Feature(name="b85_alphabet_count", desc="Count of possible base85 alphabets", type=FeatureType.Integer),
    ]

    def filter_lengths(self, lengths, alphabets: list[b64_alphabet_finder.Alphabet]) -> list[FV]:
        """Filter the list of strings based on their length."""
        return [FV(value=a.value, offset=a.offset, size=a.size) for a in alphabets if a.size in lengths]

    def execute(self, job: Job):
        """Search for alphabets in the supplied entity's content."""
        features = {}
        res: list[b64_alphabet_finder.Alphabet] = b64_alphabet_finder.find_basen_alphabets(job.get_data().read())

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
