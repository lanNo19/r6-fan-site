document.addEventListener('DOMContentLoaded', function() {
    // --- Get ALL elements needed, including those that might not exist on every page ---
    // These variables are queried once when the page loads.
    const attackButton = document.getElementById('show-attack'); // Only on /operators
    const defenseButton = document.getElementById('show-defense'); // Only on /operators
    const attackList = document.getElementById('attack-operators'); // Only on /operators
    const defenseList = document.getElementById('defense-operators'); // Only on /operators
    const operatorFilterDiv = document.querySelector('.operator-filter'); // Only on /operators
    const allOperatorItems = document.querySelectorAll('.operator-item'); // Only on /operators

    // These are global (in base.html)
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');

    // --- Helper Function to Get Current Page Path ---
    // Define this at a scope accessible by all logic blocks
    function getCurrentPagePath() {
        return window.location.pathname;
    }

    console.log(`JS Loaded. Current Page: ${getCurrentPagePath()}`); // Debugging log

    // --- Function to Filter/Display Operators (ONLY used on /operators page) ---
    // Define this function at a scope accessible by both initial load and search listeners
    function filterOperators(query) {
        console.log(`filterOperators called with query: "${query}"`); // Debugging log
        // This function assumes it is ONLY called when on the /operators page
        if (getCurrentPagePath() !== '/operators') {
             console.warn("filterOperators called on a non-/operators page. This should not happen."); // Debugging log
             return;
        }

        // Re-query elements inside the function just to be safe, though they should be in scope
        const localOperatorFilterDiv = document.querySelector('.operator-filter');
        const localAttackList = document.getElementById('attack-operators');
        const localDefenseList = document.getElementById('defense-operators');
        const localAllOperatorItems = document.querySelectorAll('.operator-item');


        if (!query || query.trim() === '') {
            // --- If query is empty (search cleared on /operators page) ---
            console.log("filterOperators: Query is empty. Showing all items."); // Debugging log
            // Show all operator items
            localAllOperatorItems.forEach(item => {
                item.style.display = 'block';
            });

            // Show the filter buttons
            if (localOperatorFilterDiv) {
                localOperatorFilterDiv.style.display = 'block';
            }

            // --- REMOVED: Lines that incorrectly reset attackList/defenseList display ---
            // if (localAttackList && localDefenseList) {
            //     localAttackList.style.display = 'block';
            //     localDefenseList.style.display = 'none';
            // }

             // Hide search results info when search is cleared
             const searchResultsInfoDiv = document.querySelector('.search-results-info');
             if (searchResultsInfoDiv) {
                  searchResultsInfoDiv.style.display = 'none';
             }


            console.log("Search cleared on Operators page, showing all operators and filters."); // Debugging log
            return;
        }

        // --- If query is NOT empty (performing search on /operators page) ---
        console.log(`filterOperators: Query is NOT empty. Fetching results for "${query}"`); // Debugging log
        // Hide the filter buttons
        if (localOperatorFilterDiv) {
            localOperatorFilterDiv.style.display = 'none';
        }
        console.log("Search active on Operators page, hiding filter buttons."); // Debugging log

        // Send search query to the backend API
        fetch(`/api/search?query=${encodeURIComponent(query)}`)
            .then(response => {
                console.log(`Fetch response status: ${response.status}`); // Debugging log
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(results => {
                console.log("Search API results:", results); // Debugging log
                console.log(`Number of results: ${results.length}`); // Debugging log

                const matchingOperatorNames = new Set(results.map(op => op.name));
                console.log("Matching operator names from API:", matchingOperatorNames); // Debugging log

                // Only process operator items if they exist (which they should on /operators)
                console.log(`Total operator items found on page: ${localAllOperatorItems.length}`); // Debugging log
                if (localAllOperatorItems.length > 0) {
                    localAllOperatorItems.forEach(item => {
                        const operatorName = item.getAttribute('data-operator-name');
                        // console.log(`Checking item: ${operatorName}`); // Optional: log every item check
                        if (matchingOperatorNames.has(operatorName)) {
                            console.log(`Showing item: ${operatorName}`); // Debugging log
                            item.style.display = 'block'; // Show matching item
                            // Ensure parent lists are visible when showing search results
                            // This is important if the lists were hidden by the toggle buttons
                            if (localAttackList) localAttackList.style.display = 'block';
                            if (localDefenseList) localDefenseList.style.display = 'block';
                        } else {
                            // console.log(`Hiding item: ${operatorName}`); // Optional: log every hidden item
                            item.style.display = 'none'; // Hide non-matching item
                        }
                    });

                    // Optional: Update search results count display
                     const searchCountSpan = document.getElementById('search-count');
                     const searchResultsInfoDiv = document.querySelector('.search-results-info');
                     if (searchCountSpan && searchResultsInfoDiv) {
                          searchCountSpan.textContent = results.length;
                          searchResultsInfoDiv.style.display = 'block'; // Show the message div
                     }


                } else {
                    console.warn("No operator items found on /operators page during filtering?"); // Debugging log
                }

                if (results.length === 0) {
                     console.log("No operators found matching the search."); // Debugging log
                     // Display "No results" message
                     const searchCountSpan = document.getElementById('search-count');
                     const searchResultsInfoDiv = document.querySelector('.search-results-info');
                     if (searchCountSpan && searchResultsInfoDiv) {
                          searchCountSpan.textContent = "0"; // Set count to 0
                          searchResultsInfoDiv.style.display = 'block'; // Show the message div
                     }
                }
            })
            .catch(error => {
                console.error('Error during search:', error); // Debugging log
                alert("Could not perform search. Please try again.");
                // Decide what to show on error - maybe show all or clear results
                filterOperators(''); // Clear search on error
            });
    }

    // --- Function to Handle Search (Global) ---
    // Define this function at a scope accessible by search listeners
    function handleSearch(query) {
         console.log(`handleSearch called with query: "${query}"`); // Debugging log
         if (!query || query.trim() === '') {
             // If query is empty:
             if (getCurrentPagePath() === '/operators') {
                 // On operators page, clear filter
                 console.log("Query empty on /operators page. Calling filterOperators('')"); // Debugging log
                 filterOperators('');
             } else {
                 // On other pages, maybe redirect to a clean operators page or do nothing.
                 // Redirecting to a clean operators page is often good UX.
                 console.log("Search cleared on a non-operators page. Redirecting to clean /operators."); // Debugging log
                 window.location.href = '/operators'; // Redirect to /operators without query
             }
             return; // Exit function
         }

        // If query is NOT empty:
        if (getCurrentPagePath() === '/operators') {
            // If on the operators page, apply the filter directly
            console.log(`Performing filter on Operators page for query: "${query}"`); // Debugging log
            filterOperators(query);
        } else {
            // If on any other page, redirect to the operators page with the query
            const redirectUrl = `/operators?query=${encodeURIComponent(query)}`;
            console.log(`Redirecting to ${redirectUrl}`); // Debugging log
            window.location.href = redirectUrl;
        }
    }


    // --- Operators Page Specific Logic (Initial Load and Toggle Buttons) ---
    // This block now handles initial query check AND toggle button listeners
    // if the elements are found (meaning we are on the /operators page).
    if (attackButton && defenseButton && attackList && defenseList && operatorFilterDiv) {
         console.log("Operators page specific elements found. Initializing."); // Debugging log

         // --- Toggle Button Listeners ---
         attackButton.addEventListener('click', function() {
             console.log("Attack button clicked (Operators page)."); // Debugging log
             attackList.style.display = 'block'; // Show Attackers container
             defenseList.style.display = 'none'; // Hide Defenders container

             // Clear search input and reset filter state when switching sides
             if (searchInput) {
                 searchInput.value = '';
             }
             // Call filterOperators('') to reset individual item display and hide search results info
             filterOperators('');
         });

         defenseButton.addEventListener('click', function() {
             console.log("Defense button clicked (Operators page)."); // Debugging log
             attackList.style.display = 'none'; // Hide Attackers container
             defenseList.style.display = 'block'; // Show Defenders container

              // Clear search input and reset filter state when switching sides
             if (searchInput) {
                 searchInput.value = '';
             }
             // Call filterOperators('') to reset individual item display and hide search results info
             filterOperators('');
         });

         // --- Initial State on /operators Page Load ---
         // Check if there's a search query in the URL and apply filter.
         console.log("Checking URL for initial query on /operators page..."); // Debugging log
         const urlParams = new URLSearchParams(window.location.search);
         const initialQuery = urlParams.get('query');

         if (initialQuery) {
             // If there's a query in the URL, put it in the search box and filter
             if (searchInput) {
                 searchInput.value = initialQuery;
             }
             console.log(`Initial query found in URL: "${initialQuery}". Applying filter.`); // Debugging log
             filterOperators(initialQuery); // Apply the filter based on the URL query
         } else {
             // If no query in URL, set initial display state (show attackers, hide defenders)
             console.log("No initial query in URL. Setting default Operators page display."); // Debugging log
             attackList.style.display = 'block';
             defenseList.style.display = 'none';
             operatorFilterDiv.style.display = 'block'; // Ensure filter buttons are visible
              // Ensure all individual operator items are visible initially within their respective lists
              // This is important if filterOperators('') isn't called on load without a query.
              allOperatorItems.forEach(item => {
                   item.style.display = 'block';
              });
         }
     } else {
         console.log("Not on Operators page or some Operators-specific elements not found."); // Debugging log
     }


    // --- Search Event Listeners (Global) ---
    // Attach listeners if global search elements exist
    if (searchInput && searchButton) {
        console.log("Global search elements found. Attaching listeners."); // Debugging log
        searchButton.addEventListener('click', function(event) {
             event.preventDefault(); // Prevent default form submission
            const query = searchInput.value.trim(); // Get query
            handleSearch(query); // Call the handler function
        });

        searchInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                console.log("Enter key pressed in search input."); // Debugging log
                event.preventDefault(); // Prevent default form submission/newline
                const query = searchInput.value.trim(); // Get query
                handleSearch(query); // Call the handler function
            }
        });

        // --- Input Listener to Clear Search ---
         searchInput.addEventListener('input', function() {
             console.log("Search input value changed."); // Debugging log
             if (searchInput.value.trim() === '') {
                 // If input is cleared, handle search with an empty query
                 console.log("Search input cleared."); // Debugging log
                 handleSearch('');
             }
         });
    } else {
        console.log("Global search elements not found on this page."); // Debugging log
    }
});
