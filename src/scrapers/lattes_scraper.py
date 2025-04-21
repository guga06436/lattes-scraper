from selenium.webdriver.common.by import By

class LattesScraper:
    """
    Scrapes data from a Lattes curriculum page.
    """

    def __init__(self, driver):
        """
        Initializes the scraper with the provided WebDriver instance.

        Args:
            driver (webdriver): The WebDriver instance used for scraping.
        """
        self.driver = driver

    def scrap_lattes_data(self):
        """
        Performs a full data scrape, extracting key details such as name, nationality,
        academic title, languages, and productions.

        Returns:
            dict: A dictionary containing the scraped data.
        """
        data = {}
        data['nome_lattes'] = self.scrap_nome_lattes()
        data['nacionalidade'] = self.scrap_nacionalidade()
        data['titulo'] = self.scrap_academic_title()
        data['idiomas'] = self.scrap_idiomas()
        data['producoes'] = self.scrap_producoes()
        return data

    def scrap_nome_lattes(self):
        """
        Scrapes the name of the person from the Lattes curriculum.

        Returns:
            str or None: The person's name or None if not found.
        """
        try:
            return self.driver.find_element(By.CLASS_NAME, "nome").text
        except Exception as e:
            print(f"Error scraping name: {e}")
            return None

    def scrap_nacionalidade(self):
        """
        Scrapes the nationality of the person from the Lattes curriculum.

        Returns:
            str or None: The nationality of the person or None if not found.
        """
        try:
            return self.driver.find_element(By.XPATH, "//b[contains(text(), 'País de Nacionalidade')]/ancestor::div[@class='layout-cell layout-cell-3 text-align-right']/following-sibling::div").text
        except Exception as e:
            print(f"Error scraping nationality: {e}")
            return None

    def scrap_academic_title(self):
        """
        Scrapes and determines the highest academic title from the curriculum (e.g., Doctorate, Master's, etc.).

        Returns:
            str or None: The highest academic title or None if not found.
        """
        title_levels = {'Doutorado': 4, 'Mestrado': 3, 'Especialização': 2, 'Graduação': 1}
        highest_title = 'Outros'
        highest_level = 0

        try:
            titulo_section = self.driver.find_element(By.XPATH, "//a[@name='FormacaoAcademicaTitulacao']/following::hr/following::div[1]")
            layout_cells = titulo_section.find_elements(By.CLASS_NAME, "layout-cell.layout-cell-9")

            for cell in layout_cells:
                full_text = cell.text.strip().lower()
                for title, level in title_levels.items():
                    if title.lower() in full_text and level > highest_level:
                        highest_title = title
                        highest_level = level
            return highest_title
        except Exception as e:
            print(f"Error scraping academic title: {e}")
            return None

    def scrap_idiomas(self):
        """
        Scrapes the list of languages spoken by the person.

        Returns:
            list[str] or None: A list of languages or None if not found.
        """
        try:
            idiomas_section = self.driver.find_element(By.XPATH, "//a[@name='Idiomas']/following-sibling::div")
            language_cells = idiomas_section.find_elements(By.CLASS_NAME, "layout-cell.layout-cell-3.text-align-right")
            return [cell.text.strip() for cell in language_cells if cell.text.strip()]
        except Exception as e:
            print(f"Error scraping languages: {e}")
            return None

    def scrap_producoes(self):
        """
        Scrapes the scientific productions listed in the curriculum.

        Returns:
            str or None: The textual representation of the productions or None if not found.
        """
        try:
            return self.driver.find_element(By.XPATH, "//a[@name='ProducoesCientificas']/following-sibling::div[1]").text
        except Exception as e:
            print(f"Error scraping productions: {e}")
            return None
