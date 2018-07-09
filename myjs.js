var i=1;
$('#add_option').on('click', function()
{
ap=$(this).parent();
    x=ap.find('#optionrow').clone(true,true);
    optionname='option'+ ++i;
    x.find('input:first').attr('name',optionname);
    x.find('.remove').attr('disabled',false);
    console.log(x);
    ap.find('#options').append(x);
    return false;

});
$('#addmore').on('click', function()
{

    x=$('#form1').clone(true);
    x.find("#myform")[0].reset();
    x.attr('id','form'+ ++i);
    x.find('#myform').attr('hidden',false);
    $('#form1').after(x);

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
    ap.find("#optioncontainer").hide();
    ap.find("#truefalsecontainer").hide();
    ap.find("#myform")[0].reset();
    $(this).prop('checked',true);
});

$('#optionrow').on('click', '.remove', function(){
    $(this).parent().remove();
    i--;
    return false; //prevent form submission
    });
$(function(){
$('#truefalsecontainer').hide();

});
$(".whichcorrect").click(function(){
$(this).prop('checked',true);
ap=$(this).parentsUntil('#optionrow');
var x=ap.find('input').val();

console.log(x);
ap.find('input.whichcorrect').prop('value',x);
ap.find('input.whichcorrect').prop('checked',True);
return false;
});
