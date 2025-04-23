document.addEventListener('DOMContentLoaded', function() {
    // Filter functionality
    const categoryFilter = document.getElementById('category-filter');
    const searchFilter = document.getElementById('search-filter');
    const skillCards = document.querySelectorAll('.skill-card');
    
    function filterSkills() {
        const category = categoryFilter.value;
        const searchTerm = searchFilter.value.toLowerCase();
        
        // If using AJAX, fetch data from server
        if (category !== 'all' || searchTerm) {
            fetch('/api/filter_skills', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    category: category,
                    search_term: searchTerm
                })
            })
            .then(response => response.json())
            .then(data => {
                updateSkillsList(data);
            })
            .catch(error => {
                console.error('Error filtering skills:', error);
            });
        } else {
            // If not using AJAX, filter directly in the DOM
            skillCards.forEach(card => {
                const cardCategory = card.dataset.category;
                const cardTitle = card.querySelector('h4').textContent.toLowerCase();
                const cardDescription = card.querySelector('.skill-description').textContent.toLowerCase();
                
                const matchesCategory = category === 'all' || cardCategory === category;
                const matchesSearch = !searchTerm || 
                                      cardTitle.includes(searchTerm) || 
                                      cardDescription.includes(searchTerm);
                
                if (matchesCategory && matchesSearch) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    }
    
    function updateSkillsList(skills) {
        const skillsList = document.getElementById('available-skills');
        
        if (!skillsList) return;
        
        // Clear current list
        skillsList.innerHTML = '';
        
        if (skills.length === 0) {
            skillsList.innerHTML = '<p>No skills match your criteria.</p>';
            return;
        }
        
        // Add each skill to the list
        skills.forEach(skill => {
            const skillElement = document.createElement('li');
            skillElement.className = 'skill-card';
            skillElement.dataset.id = skill.id;
            skillElement.dataset.category = skill.category;
            
            skillElement.innerHTML = `
                <h4>${skill.name}</h4>
                <p class="skill-teacher">Taught by: ${skill.teacher}</p>
                <p class="skill-category">${skill.category}</p>
                <p class="skill-description">${skill.description}</p>
                <form action="/request_skill/${skill.id}" method="post">
                    <button type="submit" class="request-button">Request to Learn</button>
                </form>
            `;
            
            skillsList.appendChild(skillElement);
        });
    }
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterSkills);
    }
    
    if (searchFilter) {
        searchFilter.addEventListener('input', filterSkills);
    }
    
    // Flash message timeout
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.style.display = 'none';
        }, 3000);
    }
});