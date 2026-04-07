import os
from datetime import datetime

import allure


class ScreenshotHelper:

    @staticmethod
    def take_validation_screenshot(page, step_name: str):
        """
        Takes a full-page screenshot, saves it locally, and attaches it to Allure.
        """
        folder_path = os.path.join("screenshots", "validations")
        os.makedirs(folder_path, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{step_name}_{timestamp}.png"
        file_path = os.path.join(folder_path, file_name)

        page.screenshot(path=file_path, full_page=True)

        allure.attach.file(
            source=file_path,
            name=f"Validation - {step_name}",
            attachment_type=allure.attachment_type.PNG,
        )

        print(f"\nValidation screenshot captured: {file_name}")
        return file_path
