from project.paintings.acrylic_art import AcrylicArt
from project.paintings.oil_art import OilArt
from project.paintings.watercolor_art import WatercolorArt
from project.restoration_studio import RestorationStudio


class ArtManager:
    def __init__(self):
        self.paintings = []
        self.restoration_studios = []

    def add_painting(self, painting_type: str, catalogue_number: str, price: float, status: str):
        types = {
            "OilArt": OilArt,
            "WatercolorArt": WatercolorArt,
            "AcrylicArt": AcrylicArt
        }

        if painting_type not in types:
            raise ValueError("Invalid painting type!")

        painting = types[painting_type](catalogue_number, price, status)
        self.paintings.append(painting)
        return f"{painting_type} <{catalogue_number}> has been added."

    def add_restoration_studio(self, name: str, painting_types: set):
        studio = RestorationStudio(name, painting_types)
        self.restoration_studios.append(studio)
        return f"{name} has been added as a restoration studio."

    def send_for_restoration(self, restoration_studio_name: str, painting_type: str):
        studio = next(filter(lambda s: s.name == restoration_studio_name, self.restoration_studios), None)

        if painting_type not in studio.painting_types:
            return "The studio cannot restore this painting type."

        for painting in self.paintings:
            if painting.__class__.painting_type == painting_type and painting.status == "restorable":
                self.paintings.remove(painting)
                studio.paintings.append(painting)
                return f"<{painting.catalogue_number}> was sent for restoration to {restoration_studio_name}."

        return f"There is no eligible {painting_type}."

    def process_restorations(self, restoration_studio: RestorationStudio):
        result = restoration_studio.restore()
        restored = [p for p in restoration_studio.paintings if p.status == "ready"]
        for p in restored:
            restoration_studio.paintings.remove(p)
            self.paintings.append(p)
        return result

    def remove_paintings(self):
        count = sum(1 for p in self.paintings if p.status == "irreparable")
        self.paintings = [p for p in self.paintings if p.status != "irreparable"]
        return f"Removed {count} irreparable painting/s."

    def exhibit_paintings(self):
        ready_paintings = [p for p in self.paintings if p.is_ready]
        if not ready_paintings:
            return "Exhibition postponed!"

        ready_paintings.sort(key=lambda p: p.catalogue_number)
        result = ["Art Exhibition:"]
        for p in ready_paintings:
            result.append(f"<{p.catalogue_number}> {p.__class__.painting_type} {p.price:.2f}EUR")
        return "\n".join(result)

    def manager_status(self):
        ready = sum(1 for p in self.paintings if p.status == "ready")
        restorable_count = sum(1 for p in self.paintings if p.status == "restorable")
        irreparable_count = sum(1 for p in self.paintings if p.status == "irreparable")
        result = [
            "|Art Manager|",
            f"Ready-to-display paintings: {ready}",
            f"Need restoration paintings: {restorable_count}",
            f"Irreparable paintings: {irreparable_count}",
            f"Restoration studios: {len(self.restoration_studios)}"
        ]

        studios_sorted = sorted(
            self.restoration_studios,
            key=lambda s: (-sum(1 for p in s.paintings if p.status == "restorable"), s.name)
        )

        for studio in studios_sorted:
            result.append(studio.status())

        return "\n".join(result)