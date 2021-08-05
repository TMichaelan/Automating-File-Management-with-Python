
var subFolderList = ['2.5cm', '3.5cm', '4.5cm', '6.5cm', '9.5cm']

var folderPsd = Folder('C:/Users/Admin/Desktop/Process');                                           /////// here are subfolders
var cuttingFileFolder =   Folder('D:/OneDrive/Product Files/PSD/Mockups/Cutlines');;       /////// here are folder for path ai files      
var saveFolder = Folder('C:/Users/Admin/Desktop/Process'  );                                       ////////// here are output folder
var hotFolder_1 = Folder('C:/Users/Admin/Desktop/HOT Versa - Mr. Miyagi')                   /////// here are hot folder 1
var hotFolder_2 = Folder('C:/Users/Admin/Desktop/HOT Versa - Stephanie Zinone')      /////// here are hot folder 2
var movePdfFolder = Folder('C:/Users/Admin/Desktop/Print Postage')                          //////// here is folder for movinf pdf from subfolders

//~ var folderPsd = Folder('C:/Users/user/Desktop/mark')
//~ var cuttingFileFolder =  File('C:/Users/user/Desktop/mark');
//~ var saveFolder = Folder('C:/Users/user/Desktop/mark output'  );            
//~ var hotFolder_1 = Folder('C:/Users/user/Desktop/mark output/hot folder1')
//~ var hotFolder_2 = Folder('C:/Users/user/Desktop/mark output/hot folder2')
//~ var movePdfFolder = Folder('C:/Users/user/Desktop/mark output/movePdf')


var allFiles = []
var allFilesDuplic = []
var CMYKBlack = new CMYKColor();
CMYKBlack.cyan = 0;
CMYKBlack.magenta = 0;
CMYKBlack.yellow = 0;
CMYKBlack.black = 100;



main ()


function main () {
    var delF = Folder(String(folderPsd + '/' +  '__MACOSX') )
    deleteAll(delF)
    try {delF.remove()} catch(e){}


    for (var j = 0;  j<subFolderList.length; j++) {
        
        var inputFolder = Folder(String(folderPsd + '/' + subFolderList[j]) )
        if (!inputFolder.exists){alert("Script can not find subfolder " + subFolderList[j] + ".\n Check paths of folder.")}
        movePdf(inputFolder)
        try {(Folder(String(folderPsd + '/' + subFolderList[j] + '/' + '.DS_Store') )).remove()} catch(e){}
        try {(File(String(folderPsd + '/' + subFolderList[j] + '/' + '.DS_Store') )).remove()} catch(e){}
     
        
        var actionName = subFolderList[j]
        var cuttingFile = File (cuttingFileFolder + '/' + actionName.replace('cm', '') +  ' Path.ai')

        try{processOneFolder (inputFolder, actionName, cuttingFile)} catch(e){'Alert error in subfolder: ' + subFolderList[j]}

    }
    
    fileDuplication (allFiles)
    var mixedCombo = Folder(String(folderPsd + '/' + 'Mixed Combo') )
    if (!mixedCombo.exists){alert("Script can not find Mixed Combo folder. Check paths of folder.")}
    processMixedCombo(mixedCombo)    
    split_50_50 (allFilesDuplic, hotFolder_1, hotFolder_2)

    
    alert("Process completed")
}


function movePdf(inputFolder){
    var pdfFiles = getFilesPdf(inputFolder)
    
    for (var jl = 0;  jl<pdfFiles.length; jl++) {
       pdfFiles[jl].copy ( File(String (movePdfFolder) +'/' +pdfFiles[jl].name));
    }

}

function fileDuplication (inputFolder) {
    var folderPsdFiles = inputFolder
    
    for (var f = 0;  f<folderPsdFiles.length; f++) {

        var numberCopyString = folderPsdFiles[f].name.split('_')[0]
//~         var numberCopyString = Number(folderPsdFiles[f].name.split('_')[0].replace("x", "")) -1
        var FileOriginal =folderPsdFiles[f].fullName.split('.').slice(0, -1).join(".")
        var fName = folderPsdFiles[f].name
        
        var fileExtension 
        var extRE = /\.(?:psd)$/i;
        if ( fName.match( /\.(?:pdf)$/i)) {
            fileExtension = '.pdf'
        } else if ( fName.match( /\.(?:tif)$/i)){
            fileExtension = '.tif'
        } else if ( fName.match( /\.(?:eps)$/i)){
            fileExtension = '.eps'
        }
        
        var extRE = new RegExp("x", "gi");
        if (numberCopyString.match(extRE)) {
            var numberCopy = Number(numberCopyString.replace("x", "")) -1
            
            var renameFile = String (String (FileOriginal)+ '_1_of_' + String(numberCopy+1) + fileExtension)    //// new name of a file which will be renamed
            
            allFilesDuplic.push(File(renameFile))
            for(c=0; c <numberCopy; c++){
                var newName_ = String (FileOriginal) + '_' + String(c+2) + '_of_' + String(numberCopy+1) + fileExtension;
                (File(folderPsdFiles[f] )).copy ( File (newName_));
                allFilesDuplic.push(File (newName_))
            }
            
            File(folderPsdFiles[f]).rename ( String (folderPsdFiles[f].name.split('.').slice(0, -1).join(".") + '_1_of_' + String(numberCopy+1) + fileExtension))
        
        }else {
            allFilesDuplic.push(folderPsdFiles[f])
        }
    }
}


function split_50_50 (allFiles, folder1, folder2) {
//~ alert(allFiles.join('\n'))
    var numberIdxFiles = Math.floor((allFiles.length -1)/2)
    for (var s = 0;  s<allFiles.length; s++) {
        
        if (s <= numberIdxFiles){
            File (allFiles[s]).copy ( File ( String(folder1)+ '/' +allFiles[s].name));
        } else {
            File (allFiles[s]).copy ( File ( String(folder2)+ '/' +allFiles[s].name));
        }
    }

}



function processOneFolder (folderPsd, actionName, cuttingFile) {
    
    var folderPsdFiles = getFiles(folderPsd)
    try {var docAi = open (cuttingFile)} catch (e){
        alert("Can not find illustrator file Path.ai for folder:\n" +  String(decodeURI(folderPsd)) + "\n" + "Check whether folder paths are corect and does this folder exist.")
    }
    for (var i = 0;  i<folderPsdFiles.length; i++) {
    //~ var psdOptions = preferences.photoshopFileOptions;
    //~ psdOptions.preserveLayers = true;
    //~ psdOptions.pixelAspectRatioCorrection = false;
        app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
        var docPsd = open (folderPsdFiles[i]);
        var namePsd = docPsd.name.split('.').slice(0, -1).join(".")
        app.activeDocument= docAi
        docAi.layers[0].hasSelectedArtwork = true;
        app.executeMenuCommand ('copy');
        
        app.activeDocument= docPsd
        app.executeMenuCommand ('paste')
        app.selection[0].moveToBeginning(docPsd);
        app.doScript(actionName, "Cutlines_3")
        
        addTextFrame (namePsd, docPsd, actionName)
        
        app.doScript('save_tif', "Cutlines_3")
        app.doScript('save_pdf', "Cutlines_3")
        app.doScript('save_eps', "Cutlines_3")
        
        var fileSaved_tif = File(saveFolder + '/' + namePsd + '.tif')
        if (!fileSaved_tif.exists){alert("Script can not find .tif file with this name:\n:" + String(decodeURI(fileSaved_tif)) + ".\n"+ "One of options is that action save_tif do not save as tif.\nOther option is that action do not save in the folder " + String(decodeURI(saveFolder) + "."))}
        allFiles.push(fileSaved_tif)
        
        var fileSaved_pdf = File(saveFolder + '/' + namePsd + '.pdf')
        if (!fileSaved_pdf.exists){alert("Script can not find .pdf file with this name:\n:" + String(decodeURI(fileSaved_pdf)) + ".\n"+ "One of options is that action save_pdf do not save as pdf.\nOther option is that action do not save in the folder " + String(decodeURI(saveFolder) + "."))}
        allFiles.push(fileSaved_pdf)
        
        var fileSaved_eps = File(saveFolder + '/' + namePsd + '.eps')
        if (!fileSaved_eps.exists){alert("Script can not find .eps file with this name:\n:" + String(decodeURI(fileSaved_eps)) + ".\n"+ "One of options is that action save_eps do not save as eps.\nOther option is that action do not save in the folder " + String(decodeURI(saveFolder) + "."))}
        allFiles.push(fileSaved_eps)
        
    //~     var saveFile = saveFolder + '/' + namePsd + '.pdf'
    //~     saveFileToPDF (saveFile)
    //~     presetPdf (saveFile)
        docPsd.close(SaveOptions.DONOTSAVECHANGES)
    }

    try {docAi.close(SaveOptions.DONOTSAVECHANGES)}catch(e){}

}

function processOneFile (inputPsd, actionName, cuttingFile) {
    
    try {var docAi = open (cuttingFile)} catch (e){
        alert("Can not find illustrator file Path.ai for file in Mixed Combo folder:\n" + String(decodeURI(inputPsd))+ "\n"+ "Please check file name.")
        docPsd.close(SaveOptions.DONOTSAVECHANGES)
    }

    app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
    var docPsd = open (inputPsd);
    var namePsd = docPsd.name.split('.').slice(0, -1).join(".")

    app.activeDocument= docAi
    docAi.layers[0].hasSelectedArtwork = true;
    app.executeMenuCommand ('copy');

    app.activeDocument= docPsd
    app.executeMenuCommand ('paste')
    app.selection[0].moveToBeginning(docPsd);
    app.doScript(actionName, "Cutlines_3")
    
    addTextFrame (namePsd, docPsd, actionName)
    
    app.doScript('save_tif', "Cutlines_3")
    app.doScript('save_pdf', "Cutlines_3")
    app.doScript('save_eps', "Cutlines_3")
    
    var fileSaved_tif = File(saveFolder + '/' + namePsd + '.tif')
    if (!fileSaved_tif.exists){alert("Script can not find .tif file with this name:\n:" + String(decodeURI(fileSaved_tif)) + ".\n"+ "One of options is that action save_tif do not save as tif.")}
    allFilesDuplic.push(fileSaved_tif)
    
    var fileSaved_pdf = File(saveFolder + '/' + namePsd + '.pdf')
    if (!fileSaved_pdf.exists){alert("Script can not find .pdf file with this name:\n:" + String(decodeURI(fileSaved_pdf)) + ".\n"+ "One of options is that action save_pdf do not save as pdf.")}
    allFilesDuplic.push(fileSaved_pdf)
    
    var fileSaved_eps = File(saveFolder + '/' + namePsd + '.eps')
    if (!fileSaved_eps.exists){alert("Script can not find .eps file with this name:\n:" + String(decodeURI(fileSaved_eps)) + ".\n"+ "One of options is that action save_eps do not save as eps.")}
    allFilesDuplic.push(fileSaved_eps)    
//~     var fileSaved = File(saveFolder + '/' + namePsd + '.tif')
//~     if (!fileSaved.exists){alert("Script can not find tif file with this name:\n:" + String(decodeURI(fileSaved)) + ".\n"+ "One of options is that action save_as do not save as tif.")}
//~     allFilesDuplic.push(fileSaved)

    docPsd.close(SaveOptions.DONOTSAVECHANGES)
    try {docAi.close(SaveOptions.DONOTSAVECHANGES)}catch(e){}

}

function actionMixedCombo (inputFile){
    
    var forCheck = ["2x5", "3x5", "4x5", "6x5", "9x5"]
    for (var rx = 0;  rx<forCheck.length; rx++) {
        var extRE = new RegExp(forCheck[rx], "gi");
        if (inputFile.match(extRE)) {
            return subFolderList[rx]
        }
    }
    return ""
}


function processMixedCombo(theFolder) {   


    if (theFolder instanceof File ) {
        
        var extRE = /\.(?:psd)$/i;
        var docName = theFolder.name;
        
        if (docName.match(extRE)) {
            var lastPart = String(docName.split('.').slice(0, -1).join(".").split('_').slice(-1))
            var actionName = actionMixedCombo(docName)                  ///lastPart.split('x').join(".") +'cm'
            if (actionName == ""){alert("Script can not find action for this file:\n" + String(decodeURI(theFolder)) + "\n"  + "Check file name of this file inside Mixed Combo.")}
            var cuttingFile = File (cuttingFileFolder + '/' + actionName.replace('cm', '') +  ' Path.ai')
            try{processOneFile (theFolder, actionName, cuttingFile)} catch(e){alert("Error in the file:\n" + String(decodeURI(theFolder)))}
        }
        return 
    
    } else if (theFolder instanceof Folder){

            var fileFolderArray = theFolder.getFiles();  

            for ( var i = fileFolderArray.length-1; i >= 0; i-- ) {  
               processMixedCombo (fileFolderArray[i])
            }
        return 
    }
}

function addTextFrame (inputTx, docPsd, actionName) {
    var newTextFrame = docPsd.layers[0].textFrames.add()
    newTextFrame.contents = inputTx
    newTextFrame.textRange.characterAttributes.textFont = textFonts.getByName("MyriadPro-Regular");   //("MyriadPro-Regular");   GillSans-Light
    newTextFrame.textRange.characterAttributes.size = 12;
    newTextFrame.textRange.characterAttributes.fillColor = CMYKBlack;  
    newTextFrame.position =[docPsd.artboards[0].artboardRect[0]+7, docPsd.artboards[0].artboardRect[1]-7]
    if (actionName == '9.5cm'){
        newTextFrame.rotate(-90)
        newTextFrame.position =[docPsd.artboards[0].artboardRect[2]-16, docPsd.artboards[0].artboardRect[1]-7]
    }
}



function getFiles(sourceFolder) {
	var fileArray = new Array();
	var extRE = /\.(?:psd)$/i;


	var docs = sourceFolder.getFiles();
	var len = docs.length;
	for (var i = 0; i < len; i++) {
		var doc = docs[i];

		if (doc instanceof File) {
			var docName = doc.name;
			if (docName.match(extRE)) {
				fileArray.push(doc);
			}
		}
	}
 

	return fileArray;
}

function getFilesPdf(sourceFolder) {
	var fileArray = new Array();
	var extRE = /\.(?:pdf)$/i;


	var docs = sourceFolder.getFiles();
	var len = docs.length;
	for (var i = 0; i < len; i++) {
		var doc = docs[i];

		if (doc instanceof File) {
			var docName = doc.name;
			if (docName.match(extRE)) {
				fileArray.push(doc);
			}
		}
	}
 

	return fileArray;
}



function getFolders(sourceFolder) {
	var fileArray = new Array();

	var docs = sourceFolder.getFiles();
	var len = docs.length;
	for (var i = 0; i < len; i++) {
		var doc = docs[i];

		if (doc instanceof Folder) {
				fileArray.push(doc);
		}
	}

	return fileArray;
}




function saveFileToPDF (dest) {
var doc = app.activeDocument;
if ( app.documents.length > 0 ) {
var saveName = new File ( dest );
saveOpts = new PDFSaveOptions();
//~ saveOpts.compatibility = PDFCompatibility.ACROBAT5;
saveOpts.generateThumbnails = true;
saveOpts.preserveEditability = true;
doc.saveAs( saveName, saveOpts );
}
}

function presetPdf (dest){
    var doc = app.activeDocument;
    var opts = new PDFSaveOptions();

    opts.pDFPreset = 'Mark preset';

    var saveName = new File ( dest );



    doc.saveAs ( saveName, opts );

}


function deleteFolder(inputFolder){
    var searchFiles = [] 
    findAllFiles (inputFolder, searchFiles)
//~     alert(searchFiles)
    for ( var i = searchFiles.length-1; i >= 0; i--) { 
        try {searchFiles[i].remove()} catch(e){}
    }

    var searchFolders = [] 
    findAllFolders(inputFolder, searchFolders)
    alert(searchFolders)
    for ( var i = searchFolders.length-1; i >= 0; i--) { 
//~     while (searchFolders.length == 0){
        try {searchFolders[i].remove()} catch(e){}
    }
    try {inputFolder.remove()} catch(e){}
}

function findAllFiles(theFolder, AllFiles) {  // function which search for for files in subfolder of choosen folder in recursive way 

    var fileFolderArray = theFolder.getFiles();  

    for ( var i = 0; i < fileFolderArray.length; i++ ) {  
        if (fileFolderArray[i] instanceof File ) {
            AllFiles.push(fileFolderArray[i])
        }else{  
            findAllFiles (fileFolderArray[i], AllFiles) 
        }  
    }
}


function findAllFolders(theFolder, AllFolders) {  // function which search for for files in subfolder of choosen folder in recursive way 

    var fileFolderArray = theFolder.getFiles();  

    for ( var i = 0; i < fileFolderArray.length; i++ ) {  
        if (fileFolderArray[i] instanceof Folder && fileFolderArray[i].length ==0) {
            AllFolders.push(fileFolderArray[i])
        }else{  
            findAllFiles (fileFolderArray[i], AllFolders) 
        }  
    }
}

function deleteAll(theFolder) {   


    if (theFolder instanceof File ) {
        return theFolder.remove()
    
    } else if (theFolder instanceof Folder){
        
            var fileFolderArray = theFolder.getFiles();  

            for ( var i = fileFolderArray.length-1; i >= 0; i-- ) {  
               deleteAll(fileFolderArray[i])
            }
        return theFolder.remove()
    }
}


//~ function exportFileToPSD (dest) {
//~ if ( app.documents.length > 0 ) {
//~ var exportOptions = new ExportOptionsTIFF();
//~ var type = ExportType.TIFF;
//~ var fileSpec = new File(dest);
//~ exportOptions.resolution = 300;
//~ exportOptions.byteOrder = TIFFByteOrder.IBMPC;
//~ exportOptions.IZWCompression = false;
//~ app.activeDocument.exportFile( fileSpec, type, exportOptions );
//~ }
//~ }