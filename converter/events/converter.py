import os, zipfile, tarfile, py7zr
from io import BytesIO
from google.cloud import storage


class CustomFileCompressor:
    """Base class for handling compressed files"""

    compressor_create_func = None
    compressor_insert_func: str = ""
    new_format: str = ""
    mode: str = ""

    def compress_file(self, file: bytes, file_name: str, old_format: str):

        print(f"Compressing {file_name}.{old_format} to {self.new_format}")

        file_obj = BytesIO(file)
        compressed_file = BytesIO()

        with self.compressor_create_func(compressed_file, self.mode) as compressor:
            compressor.writestr(f"{file_name}.{old_format}", file_obj.getvalue())

        compressed_file.seek(0)
        compressed_file_bytes = compressed_file.getvalue()
        compressed_file.close()
        file_obj.close()

        # Upload the compressed file to the Cloud Storage bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket("conversion-files-bucket")
        blob = bucket.blob(f"{file_name}.{self.new_format}")
        with open(f"{file_name}.{self.new_format}", "wb") as f:
            f.write(compressed_file_bytes)
        blob.upload_from_filename(f"{file_name}.{self.new_format}")
        os.remove(f"{file_name}.{self.new_format}")

        print(f"Completed Compression to {self.new_format}")
        return compressed_file_bytes


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
