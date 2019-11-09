__G__ = "(G)bd249ce4"

from ..logger.logger import logstring,verbose,verbose_flag
from ..mics.qprogressbar import progressbar
from ..mics.funcs import getwords
from pefile import PE,RESOURCE_TYPE,DIRECTORY_ENTRY
from hashlib import md5
from magic import from_file
from datetime import datetime
from M2Crypto import BIO, m2, SMIME, X509

class WindowsPe:
    @verbose(verbose_flag)
    @progressbar(True,"Starting WindowsPe")
    def __init__(self,qbs):
        '''
        initialize class

        Args:
            qbs: is QBStrings class, needed for string description
        '''
        self.qbs = qbs

    @verbose(verbose_flag)
    def whattype(self,pe) -> str:
        '''
        check file exe or dll or driver

        Args:
            pe: pe object

        Return:
            True type
        '''
        if pe.is_exe():
            return "exe"
        elif pe.is_dll():
            return "dll"
        elif pe.is_driver():
            return "driver"

    @verbose(verbose_flag)
    def checkifsinged(self,pe) -> list:
        '''
        check file if it has Signature or not

        Args:
            pe: pe object

        Return:
            list of signatures
        '''
        i = 0
        _list = []
        _extracted = {}
        Problems = False 
        address = pe.OPTIONAL_HEADER.DATA_DIRECTORY[DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_SECURITY']].VirtualAddress
        if address != 0:
            try:
                sig = pe.write()[address+8:]
                m2cbio = BIO.MemoryBuffer(bytes(sig))
                if m2cbio:
                    pkcs7bio = m2.pkcs7_read_bio_der(m2cbio.bio_ptr())
                    if pkcs7bio:
                        pkcs7 = SMIME.PKCS7(pkcs7bio)
                        for cert in pkcs7.get0_signers(X509.X509_Stack()):
                            tempcert = "CERT_{}".format(i)
                            _extracted[tempcert] = { "CommonName":None,
                                                     "OrganizationalUnit":None,
                                                     "Organization":None,
                                                     "Locality":None,
                                                     "StateOrProvinceName":None,
                                                     "CountryName":None,
                                                     "Start":None,
                                                     "Ends":None,
                                                     "SerialNumber":None}
                            try:
                                _extracted[tempcert]["CommonName"] = cert.get_subject().CN
                            except:
                                pass
                            try:
                                _extracted[tempcert]["OrganizationalUnit"] = cert.get_subject().OU
                            except:
                                pass
                            try:
                                _extracted[tempcert]["Organization"] = cert.get_subject().O
                            except:
                                pass
                            try:
                                _extracted[tempcert]["Locality"] = cert.get_subject().L
                            except:
                                pass
                            try:
                                _extracted[tempcert]["StateOrProvinceName"] = cert.get_subject().S
                            except:
                                pass
                            try:
                                _extracted[tempcert]["CountryName"] = cert.get_subject().C
                            except:
                                pass
                            try:
                                _extracted[tempcert]["Email"] = cert.get_subject().Email
                            except:
                                pass
                            try:
                                _extracted[tempcert]["Start"] = str(cert.get_not_before())
                            except:
                                pass
                            try:
                                _extracted[tempcert]["Ends"] = str(cert.get_not_after())
                            except:
                                pass
                            try:
                                _extracted[tempcert]["SerialNumber"] = cert.get_serial_number()
                                _extracted[tempcert]["SerialNumberMD5"] = cert.get_fingerprint('md5').lower().rjust(32, '0')
                            except:
                                pass
            except:
                Problems = True
            sighex = "".join("{:02x}".format(x) for x in sig)
            _list.append({"Issues":Problems,
                          "SignatureHex":sighex})
        return _list,_extracted

    @verbose(verbose_flag)
    def findentrypointfunction(self,pe, rva) -> str:
        '''
        find entery point in sections

        Args:
            pe: pe object

        Return:
            section name
        '''
        for section in pe.sections:
            if section.contains_rva(rva):
                return section

    @verbose(verbose_flag)
    def getdlls(self,pe) -> list:
        '''
        get dlls

        Args:
            pe: pe object

        Return:
            list of dlls
        '''
        _list = []
        for dll in pe.DIRECTORY_ENTRY_IMPORT:
            if dll.dll.decode("utf-8",errors="ignore") not in str(_list):
                _list.append({"Dll":dll.dll.decode("utf-8",errors="ignore"),
                              "Description":""})
        return _list

    @verbose(verbose_flag)
    def getsections(self,pe) -> list:
        '''
        get sections

        Args:
            pe: pe object

        Return:
            list of sections
        '''
        _list = []
        for section in pe.sections:
            _list.append({  "Section":section.Name.decode("utf-8",errors="ignore").strip("\00"),
                            "MD5":section.get_hash_md5(),
                            "Description":""})
        return _list

    @verbose(verbose_flag)
    def getimportedfunctions(self,pe) -> list:
        '''
        get import functions

        Args:
            pe: pe object

        Return:
            list of import functions and their info
        '''
        _list = []
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for func in entry.imports:
                    #print({entry.dll.decode("utf-8",errors="ignore"):func.name.decode("utf-8",errors="ignore")})
                    _list.append({ "Dll":entry.dll.decode("utf-8",errors="ignore"),
                                                "Function":func.name.decode("utf-8",errors="ignore"),
                                                "Description":""})
        return _list

    @verbose(verbose_flag)
    def getexportedfunctions(self,pe) -> list:
        '''
        get export functions

        Args:
            pe: pe object

        Return:
            list of export functions and their info
        '''
        _list = []
        if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
            for func in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                _list.append({ "Function":func.name.decode("utf-8",errors="ignore"),
                                           "Description":""})
        return _list

    @verbose(verbose_flag)
    def getrecourse(self,pe) -> (list,str):
        '''
        get resources

        Args:
            pe: pe object

        Return:
            list of resources and their info
            the manifest resource decoded
        '''
        manifest = ""
        _list = []
        if hasattr(pe, "DIRECTORY_ENTRY_RESOURCE"):
            for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if resource_type.name is not None:
                    name = resource_type.name
                else:
                    name = RESOURCE_TYPE.get(resource_type.struct.Id)
                if name == None:
                    name = resource_type.struct.Id
                if hasattr(resource_type, "directory"):
                    for resource_id in resource_type.directory.entries:
                        if hasattr(resource_id, "directory"):
                            for resource_lang in resource_id.directory.entries:
                                resourcedata = pe.get_data(resource_lang.data.struct.OffsetToData, resource_lang.data.struct.Size)
                                if name == "RT_MANIFEST":
                                    try:
                                        manifest = resourcedata.decode("utf-8",errors="ignore")
                                    except:
                                        pass
                                sig = ""
                                if len(resourcedata) >= 12:
                                    sig = "".join("{:02x}".format(x) for x in resourcedata[:12])
                                _list.append({  "Resource":name,
                                                    "Offset":hex(resource_lang.data.struct.OffsetToData),
                                                    "MD5":md5(resourcedata).hexdigest(),
                                                    "Sig":sig,
                                                    "Description":""})
        return _list,manifest



    @verbose(verbose_flag)
    def getCharacteristics(self,pe) -> dict:
        '''
        get characteristics of file

        Args:
            pe: pe object

        Return:
            dict contains key and value
        '''
        x = {"High Entropy":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_HIGH_ENTROPY_VA,
             "aslr":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE,
             "Force Integrity":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_FORCE_INTEGRITY,
             "dep":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_NX_COMPAT,
             "seh":not pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_NO_SEH,
             "No Bind":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_NO_BIND,
             "cfg":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_GUARD_CF,
             "No Isolation":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_NO_ISOLATION,
             "App Container":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_APPCONTAINER,
             "wdm Driver":pe.OPTIONAL_HEADER.IMAGE_DLLCHARACTERISTICS_WDM_DRIVER}
        return x

    @verbose(verbose_flag)
    def getdebug(self,pe) -> list:
        '''
        get debug directory 

        Args:
            pe: pe object

        Return:
            list of pdb file names
        '''
        _list = []
        if hasattr(pe, "DIRECTORY_ENTRY_DEBUG"):
            for i in pe.DIRECTORY_ENTRY_DEBUG:
                _list.append({  "Name":i.entries.PdbFileName,
                                "Description":""})
        return _list

    @verbose(verbose_flag)
    def checkpesig(self,data) -> bool:
        '''
        check mime is exe or msi

        Args:
            data: data dict

        Return:
            True if exe or msi
        '''
        if  data["Details"]["Properties"]["mime"] == "application/x-dosexec" or \
            data["Details"]["Properties"]["mime"] == "application/x-msi":
            return True

    @verbose(verbose_flag)
    @progressbar(True,"Analyzing PE file")
    def getpedeatils(self,data):
        '''
        start analyzing exe logic, add descriptions and get words and wordsstripped from the file 

        Args:
            data: data dict
        '''
        data["PE"] = {  "General" : {},
                        "Characteristics":{},
                        "Singed":[],
                        "SignatureExtracted":{},
                        "Sections":[],
                        "Dlls":[],
                        "Resources":[],
                        "Imported functions":[],
                        "Exported functions":[],
                        "Debug":[],
                        "Manifest":"",
                        "_General": {},
                        "_Characteristics": {},
                        "_Singed":["Issues","SignatureHex"],
                        "__SignatureExtracted":{},
                        "_Sections":["Section","MD5","Description"],
                        "_Dlls":["Dll","Description"],
                        "_Resources":["Resource","Offset","MD5","Sig","Description"],
                        "_Imported functions":["Dll","Function","Description"],
                        "_Exported functions":["Dll","Function","Description"],
                        "_Debug":["Name","Description"],
                        "_Manifest":""}
        pe = PE(data["Location"]["File"])
        ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        section = self.findentrypointfunction(pe,ep)
        sig = section.get_data(ep, 12)
        singinhex = "".join("{:02x}".format(x) for x in sig)
        #self.getdebug(pe)
        data["PE"]["General"] = {   "PE Type" : self.whattype(pe),
                                    "Entropy": section.get_entropy(),
                                    "Entrypoint": pe.OPTIONAL_HEADER.AddressOfEntryPoint,
                                    "Entrypoint Section":section.Name.decode("utf-8",errors="ignore").strip("\00"),
                                    "verify checksum":pe.verify_checksum(),
                                    "Sig":singinhex,
                                    "imphash":pe.get_imphash(),
                                    "warning":pe.get_warnings(),
                                    "Timestamp":datetime.fromtimestamp(pe.FILE_HEADER.TimeDateStamp)}
        data["PE"]["Characteristics"] = self.getCharacteristics(pe)
        data["PE"]["Singed"],data["PE"]["SignatureExtracted"] = self.checkifsinged(pe)
        data["PE"]["Sections"] = self.getsections(pe)
        data["PE"]["Dlls"] = self.getdlls(pe)
        data["PE"]["Resources"],data["PE"]["Manifest"] = self.getrecourse(pe)
        data["PE"]["Imported functions"] = self.getimportedfunctions(pe)
        data["PE"]["Exported functions"] = self.getexportedfunctions(pe)
        self.qbs.adddescription("WinApis",data["PE"]["Imported functions"],"Function")
        self.qbs.adddescription("ManHelp",data["PE"]["Imported functions"],"Function")
        self.qbs.adddescription("WinDlls",data["PE"]["Dlls"],"Dll")
        self.qbs.adddescription("WinSections",data["PE"]["Sections"],"Section")
        self.qbs.adddescription("WinResources",data["PE"]["Resources"],"Resource")
        getwords(data,data["Location"]["File"])