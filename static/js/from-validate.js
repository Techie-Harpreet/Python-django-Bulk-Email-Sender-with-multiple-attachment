
  function checkfile(sender) {

      var validExts = new Array(".xlsx", ".xls",".csv");
      var fileExt = sender.value;
      fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
      if (validExts.indexOf(fileExt) < 0) {
        alert("Invalid file selected, valid files are of " +
                 validExts.toString() + " types.");
                 document.getElementById('formFile').value = ''
        return false;
      }
      else return true;
  }
