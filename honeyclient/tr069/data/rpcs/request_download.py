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
