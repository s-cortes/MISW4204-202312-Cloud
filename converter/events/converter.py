import os, zipfile, tarfile, py7zr


class CustomFileCompressor:
    """Base class for handling compressed files"""

    compressor_create_func = None
    compressor_insert_func: str = ""
    new_format: str = ""
    mode: str = ""

    def compress_file(self, path: str, file_name: str, old_format: str):
        """
        This function handles the logic for compressing a specific file
        and storing it on a given path.

        This function requires the initialization of its class attributes,
        therefore, it cannot be called directly from CustomFileCompressor,
        but rather by one of its childe classes

        Args:
            path (str): path where files is stored and will be compressed
            file_name (str): name of the file to be compressed
            old_format (str): current file format
        """
        print(f"Compressing {file_name}.{old_format} to {self.new_format}")

        input_path = os.path.join(path, f"{file_name}.{old_format}")
        output_path = os.path.join(path, f"{file_name}.{self.new_format}")

        with self.compressor_create_func(output_path, self.mode) as compressor:
            getattr(compressor, self.compressor_insert_func)(input_path)

        print(f"Completed Compression to {output_path}")


class CustomZipCompressor(CustomFileCompressor):
    """Custom class for compressing files into ZIP format"""

    compressor_create_func = zipfile.ZipFile
    compressor_insert_func = "write"
    new_format = "zip"
    mode = "w"


class CustomSevenZipCompressor(CustomFileCompressor):
    """Custom class for compressing files into 7Zip format"""

    compressor_create_func = py7zr.SevenZipFile
    compressor_insert_func = "write"
    new_format = "7z"
    mode = "w"


class CustomTarGZCompressor(CustomFileCompressor):
    """Custom class for compressing files into TAR GZ format"""

    compressor_create_func = tarfile.open
    compressor_insert_func = "add"
    new_format = "tar.gz"
    mode = "w:gz"


class CustomTarBZTwoCompressor(CustomFileCompressor):
    """Custom class for compressing files into TAR BZ2 format"""

    compressor_create_func = tarfile.open
    compressor_insert_func = "add"
    new_format = "tar.bz2"
    mode = "w:bz2"


class CustomFileCompressorFactory:
    """
    Factory pattern for instantiating the appropriate compressor class
    """

    @staticmethod
    def get_custom_file_converter(format_type: str) -> CustomFileCompressor:
        """
        Factory function for selecting the appropriate compressor class
        using a specific compression format type.

        Args:
            format_type (str): compression format type

        Returns:
            CustomFileCompressor: The corresponding compressor class
        """
        converters = {
            "zip": CustomZipCompressor,
            "7z": CustomSevenZipCompressor,
            "tar.gz": CustomTarGZCompressor,
            "tar.bz2": CustomTarBZTwoCompressor,
        }
        if format_type not in converters:
            raise KeyError(
                f"Could not instantiate a file converter for type {format_type}"
            )

        return converters[format_type]()
