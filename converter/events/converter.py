

class CustomFileConverter:
    """Base class for handling compressed files"""

    def decompress_file(self, input_path: str, output_path: str):
        """
        Base method for decompressing a file. This should be called
        strictly from child classes.

        Args:
            input_path (str): path where the compressed file is located
            output_path (str): path where resulting files will be stored
        """
        pass

    def compress_file(self, input_path: str, output_path: str):
        """_summary_

        Args:
            input_path (str): path where files are currently stored at
            output_path (str): path for the compressed to be located
        """
        pass


class CustomZipConverter(CustomFileConverter):
    """"""



class CustomSevenZipConverter(CustomFileConverter):
    """"""



class CustomTarGZConverter(CustomFileConverter):
    """"""



class CustomTarBZTwoConverter(CustomFileConverter):
    """"""


class CustomFileConverterFactory:
    """"""

    @staticmethod
    def get_custom_file_converter(format: str) -> CustomFileConverter:
        """_summary_

        Args:
            format (str): _description_

        Returns:
            CustomFileConverter: _description_
        """
        converters = {
            "zip": CustomZipConverter,
            "7z": CustomSevenZipConverter,
            "tar.gz": CustomTarGZConverter,
            "tar.bz2": CustomTarBZTwoConverter,
        }
        if format not in converters:
            raise KeyError()

        return converters[format]

