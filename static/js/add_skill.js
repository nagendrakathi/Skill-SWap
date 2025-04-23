document.addEventListener('DOMContentLoaded', function() {
    const addSkillForm = document.getElementById('add-skill-form');
    
    if (addSkillForm) {
        addSkillForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Name validation
            const name = document.getElementById('name');
            const nameError = document.getElementById('name-error');
            
            if (name.value.trim() === '') {
                nameError.textContent = 'Skill name is required';
                isValid = false;
            } else if (name.value.length < 3) {
                nameError.textContent = 'Skill name must be at least 3 characters long';
                isValid = false;
            } else {
                nameError.textContent = '';
            }
            
            // Category validation
            const category = document.getElementById('category');
            const categoryError = document.getElementById('category-error');
            
            if (category.value === '') {
                categoryError.textContent = 'Please select a category';
                isValid = false;
            } else {
                categoryError.textContent = '';
            }
            
            // Description validation
            const description = document.getElementById('description');
            const descriptionError = document.getElementById('description-error');
            
            if (description.value.trim() === '') {
                descriptionError.textContent = 'Description is required';
                isValid = false;
            } else if (description.value.length < 20) {
                descriptionError.textContent = 'Description should be at least 20 characters long';
                isValid = false;
            } else {
                descriptionError.textContent = '';
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});