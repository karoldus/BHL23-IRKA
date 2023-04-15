

function fetchPackages() {
    fetch('http://localhost:8000/packages')
      .then(response => response.json())
      .then(data => {
        const packages = data.map(package => `
          <tr>
            <td>${package.id}</td>
            <td>${package.height}</td>
            <td>${package.destination}</td>
          </tr>
        `).join('');
  
        document.querySelector("#package-list").innerHTML = packages;
      })
      .catch(error => console.error(error));
  }
  
  // Fetch packages every 2 seconds
  fetchPackages();
  setInterval(fetchPackages, 2000);
  