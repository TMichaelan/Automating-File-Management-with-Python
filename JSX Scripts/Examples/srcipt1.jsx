#target illustrator

var docSelected = app.activeDocument.selection;
if ( docSelected.length > 0 ) {
var actionName = prompt("Which action do you want to run?", "Cut");
var set = prompt("Which set is your action in?", "Cut Lines and Print PC");
for ( i = 0; i < docSelected.length; i++ ) {
docSelected[i].selected = false;
}
app.activeDocument.selection = null;
for ( i = 0; i < docSelected.length; i++ ) {
docSelected[i].selected = true;
app.doScript(actionName, set)
docSelected[i].selected = false;
app.activeDocument.selection = null;
}
} else {
alert( "Please select one or more art objects" );
} 