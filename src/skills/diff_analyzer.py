class DiffAnalyzer:
    """Custom Skill: Processes PR file payloads into structured diffs."""

    @staticmethod
    def extract_patch_payload(files) -> str:
        diff_payload = ""
        for file in files:
            if file.status == "removed" or not file.patch:
                continue
            diff_payload += f"\n--- File: {file.filename} ---\n{file.patch}\n"
        return diff_payload
