var i=1;
$( document ).ready(function() {
var i=0;
$('#add_option').on('click', function()
{

ap=$(this).parent();
    x=ap.find('#optionrow:first').clone(true,true);
    optionname='option'+ ++i;
    x.find('input:first').attr('name',optionname);
    x.find('input:last').attr('value',optionname);
    x.find('#remove').attr('disabled',false);
    console.log(x);
    ap.find('#options').append(x);
    return false;

});
$('#optionrow').on('click', '#remove', function(){
    $(this).parent().remove();
    i--;
    return false; //prevent form submission
    });
    });

//
$('#addmore').on('click', function()
{   $('#addmore').hide();
    $("#myform")[0].reset();
    $('#myform').show();


});
<!--ap=actualparent-->
$("#mcq").click(function(){

ap=$(this).parentsUntil('#myform').parent().parent();
ap.find("#optioncontainer").show();
ap.find('#truefalsecontainer').hide();
ap.find("#truefalsecontainer :input").prop('required',null);
ap.find("#myform")[0].reset();
$(this).prop('checked',true);
});

$("#truefalse").click(function(){

ap=$(this).parentsUntil('#myform').parent().parent();
ap.find('#optioncontainer').hide();
ap.find("#optioncontainer :input").prop('required',null);
ap.find("#truefalsecontainer").show();
ap.find("#myform")[0].reset();
$(this).prop('checked',true);


});
$("#subjective").click(function()
{
    ap=$(this).parentsUntil('#myform').parent().parent();
    ap.find("#optioncontainer :input").prop('required',null);
    ap.find("#truefalsecontainer :input").prop('required',null);
    ap.find("#optioncontainer").hide();
    ap.find("#truefalsecontainer").hide();
    ap.find("#myform")[0].reset();
    $(this).prop('checked',true);
});

//hide at first
$(function(){
$('#truefalsecontainer').hide();
$('#addmore').hide();

});