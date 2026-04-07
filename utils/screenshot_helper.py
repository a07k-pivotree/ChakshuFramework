import os
from datetime import datetime


class ScreenshotHelper:

    @staticmethod
    def take_validation_screenshot(page, step_name: str):
        """
        Takes a full-page screenshot and saves it in the screenshots/validations folder.
        """
        # 1. Define the folder path and create it if it doesn't exist
        folder_path = os.path.join("screenshots", "validations")
        os.makedirs(folder_path, exist_ok=True)

        # 2. Generate a clean timestamp (e.g., 2026-04-06_15-30-05)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # 3. Create the final file name and path
        file_name = f"{step_name}_{timestamp}.png"
        file_path = os.path.join(folder_path, file_name)

        # 4. Tell Playwright to take the screenshot
        page.screenshot(path=file_path, full_page=True)

        print(f"\n📸 Validation screenshot captured: {file_name}")