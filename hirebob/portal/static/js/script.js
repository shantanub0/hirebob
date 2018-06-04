var validImageExtensions = [".jpg", ".jpeg", ".bmp", ".gif", ".png"];
var validResumeExtensions = [".pdf", ".doc", ".rtf", ".txt", ".odf", ".docx"]
function Validate(oForm, ext) {
    var arrInputs = oForm.getElementsByTagName("input");
    for (var i = 0; i < arrInputs.length; i++) {
        var oInput = arrInputs[i];
        if (oInput.type == "file") {
            var sFileName = oInput.value;
            if (sFileName.length > 0) {
                var blnValid = false;
                for (var j = 0; j < ext.length; j++) {
                    var sCurExtension = ext[j];
                    if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                        blnValid = true;
                        break;
                    }
                }

                if (!blnValid) {
                    alert("Sorry, " + sFileName + " is invalid, allowed extensions are: " + ext.join(", "));
                    return false;
                }
            }
        }
    }

    return true;
}