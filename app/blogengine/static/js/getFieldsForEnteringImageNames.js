files = document.getElementById('files');
element_before_will_be_added_input = document.getElementById('sendPost');
parent_element = element_before_will_be_added_input.parentNode;

function get_fields_for_entering_image_names() {
	file_list = files.files;
	for (var i = 0; i < file_list.length; i++){
		var newInput = document.createElement('input');
	    newInput.id = `image_${i}`;
	    newInput.setAttribute('name', `image_${i}`);
	    newInput.setAttribute('value', `${file_list[i].name}`);

	    parent_element.appendChild(newInput);
	    parent_element.appendChild(
	    	parent_element.removeChild(element_before_will_be_added_input)
	    );
	}
}

files.addEventListener('change', get_fields_for_entering_image_names);
