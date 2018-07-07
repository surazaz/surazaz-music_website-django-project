
var i=1;
$('#addmore').on('click', function()
{

    x=$('#form1').clone(true);
    x.find("#myform")[0].reset();
    x.attr('id','form'+ ++i);
    $('#form1').after(x);

});
<!--ap=actualparent-->
$("#mcq").click(function(){

ap=$(this).parentsUntil('#myform').parent().parent();
ap.find("#optioncontainer").show();
ap.find('#truefalsecontainer').hide();
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

var i=1;
    $('#add_option').on('click', function() {
    i++;
    ap=$(this).parentsUntil('#myform').parent().parent();

    var xyz='<div class="row"><div class="col"><input type="text" name="option'+i+'"><button class="remove">x</button></div>'
    ap.find('#options').append(xyz);
    return false; //prevent form submission
});
$('#options').on('click', '.remove', function(){
    $(this).parent().remove();
    i--;
    return false; //prevent form submission
    });

