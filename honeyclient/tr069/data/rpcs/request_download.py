import datetime
from typing import Optional

from .. import soap


def make_request_download(
        file_type: str = "1 Firmware Upgrade Image",
        file_type_arg=None
) -> str:
    """Create a RequestDownload RPC"""
    if file_type_arg is None:
        file_type_arg = {}
    args = [
        f"""
        <ArgStruct>
            <Name>{name}</Name>
            <Value>{value}</Value>
        </ArgStruct>
        """
        for name, value in file_type_arg.items()
    ]
    return soap.soapify(f"""
        <cwmp:RequestDownload>
            <FileType>{file_type}</FileType>
            <FileTypeArg soap-enc:arrayType="cwmp:ArgStruct[{len(file_type_arg)}]">
                {"".join(args)}
            </FileTypeArg>
        </cwmp:RequestDownload>
    """)


def make_download_response(
        status: int = 0,
        start_time: Optional[datetime.datetime] = None,
        complete_time: Optional[datetime.datetime] = None
) -> str:
    """Create a DownloadResponse"""
    if start_time is None:
        start_time = datetime.datetime.now()
    if complete_time is None:
        complete_time = datetime.datetime.now()
    return soap.soapify(f"""
        <cwmp:DownloadResponse>
            <Status>{status}</Status>
            <StartTime>{start_time.isoformat()}</StartTime>
            <CompleteTime>{complete_time.isoformat()}</CompleteTime>
        </cwmp:DownloadResponse>
    """)
