function changeAction(val){
	var file_type = document.getElementById('file_type').value;
	var file = document.getElementById('file');
	if (file_type == "txt" || file_type == "pdf"){
		file.style.display = 'block';
	}
	else if (file_type != "txt" || file_type != "pdf"){
		file.style.display = 'none';
	}
}

$(function() {
	$('a#button').bind('click', function() {
		i = 0;
		interval = setInterval(function() {
		    i = ++i % 4;
		    $('#header h1 a').html("Loading"+Array(i+1).join("."));
		}, 400);
		$.getJSON('/summarized', {
		  title: $('input[name="title"]').val(),
		  file_type: $('#file_type :selected').val(),
		  file: $('input[name="file"]').val(),
		  algorithm: $('#algorithm :selected').val(),
		  summary_size: $('input[name="summary_size"]').val(),
		}, function(data) {
			clearInterval(interval);
			$('#header h1 a').html(data.title + ' Summarized');
			$('#original').val(data.original);
			$('#summary').val(data.summary);	
		});
		return false;
	});
});

function copy_text(){
	var copyText = document.getElementById("summary").value;
	copyText.select();
	copyText.setSelectionRange(0, 99999);
	document.execCommand("copy");
	alert("Summary Copied to Clipboard");
}