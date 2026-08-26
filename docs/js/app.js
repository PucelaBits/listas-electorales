const DATA_FILE_URL = 'data/electoral_data.csv.gz'; 

// Global state
let rawData = [];
let filteredData = [];
let currentPage = 1;
let rowsPerPage = 50;
const tomSelects = {
    electionType: null,
    province: null,
    municipality: null
};

const DOM = {
    initialLoader: document.getElementById('initial-loader'),
    loadingText: document.getElementById('loading-text'),
    appInterface: document.getElementById('app-interface'),
    dataYearRangeText: document.getElementById('data-year-range-text'),
    
    searchInput: document.getElementById('searchInput'),
    partyInput: document.getElementById('partyInput'),
    electionTypeFilter: document.getElementById('electionTypeFilter'),
    provinceFilter: document.getElementById('provinceFilter'),
    municipalityFilter: document.getElementById('municipalityFilter'),
    yearMinFilter: document.getElementById('yearMinFilter'),
    yearMaxFilter: document.getElementById('yearMaxFilter'),
    substituteFilter: document.getElementById('substituteFilter'),
    electedFilter: document.getElementById('electedFilter'),
    tableHeaderCols: document.getElementById('tableHeaderCols'),
    tableBodyCols: document.getElementById('tableBodyCols'),
    tableHeaderScroll: document.querySelector('.table-header-scroll'),
    tableBodyScroll: document.querySelector('.table-body-scroll'),
    
    tableBody: document.getElementById('tableBody'),
    resultsCount: document.getElementById('results-count'),
    rowsPerPageSelect: document.getElementById('rowsPerPage'),
    
    prevBtn: document.getElementById('prevBtn'),
    nextBtn: document.getElementById('nextBtn'),
    pageInput: document.getElementById('pageInput'),
    totalPagesText: document.getElementById('totalPagesText'),

    downloadLinkBtn: document.getElementById('download-link')
};

const normalizeString = (str) => {
    if (!str) return "";
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
};

const prettifyElectionType = (val) =>
    val.split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');


async function loadData() {
    try {
        DOM.loadingText.innerText = "Descargando base de datos...";
        const response = await fetch(DATA_FILE_URL);
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

        DOM.downloadLinkBtn.href = DATA_FILE_URL;
        
        const arrayBuffer = await response.arrayBuffer();
        
        DOM.loadingText.innerText = "Descomprimiendo datos...";
        await new Promise(res => setTimeout(res, 50)); 
        let textData = pako.inflate(new Uint8Array(arrayBuffer), { to: 'string' });

        DOM.loadingText.innerText = "Indexando registros...";
        
        Papa.parse(textData, {
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                rawData = results.data.map(row => {
                    const partyFull = row.acronym ? `${row.acronym} - ${row.name}` : row.name;
                    return {
                        ...row,
                        _partyFull: partyFull,
                        _partyFullNormalized: normalizeString(partyFull), 
                        _searchName: normalizeString(row.full_name)
                    };
                });

                filteredData = rawData;
                
                initFilters();
                renderTable();
                setupEventListeners();

                DOM.initialLoader.classList.add('hidden');
                DOM.appInterface.classList.remove('hidden');
            }
        });

    } catch (error) {
        console.error(error);
        DOM.loadingText.innerHTML = `<span style="color: var(--danger); font-weight: 600;">Error:</span> No se pudo cargar el archivo.<br>Asegúrate de que <code>${DATA_FILE_URL}</code> existe.`;
        document.querySelector('.loader').style.display = 'none';
    }
}

function initFilters() {
    const provinces = new Set();
    const municipalities = new Set();
    const years = new Set();
    const electionTypes = new Set();

    rawData.forEach(row => {
        if (row.province) provinces.add(row.province);
        if (row.municipality) municipalities.add(row.municipality);
        if (row.year) years.add(row.year);
        if (row.election_type) electionTypes.add(row.election_type);
    });

    const tomSelectConfig = {
        create: false,
        sortField: { field: "text", direction: "asc" },
        placeholder: "Filtrar...",
        maxOptions: 100,
        dropdownParent: 'body'
    };

    // Unified populateSelect function for both Native and TomSelect
    const populateSelect = (selectElement, setValues) => {
        selectElement.innerHTML = ''; 

        // Create a universal hidden placeholder
        const defaultOpt = new Option('Filtrar...', '');
        defaultOpt.disabled = true;
        defaultOpt.selected = true;
        defaultOpt.hidden = true;
        selectElement.appendChild(defaultOpt);

        Array.from(setValues).sort().forEach(val => {
            selectElement.appendChild(new Option(val, val));
        });
    };

    // Shared column geometry for the header and body tables: identical <col>
    // widths keep both tables aligned no matter which one is horizontally scrolled.
    const COLUMN_WIDTHS = [260, 140, 190, 200, 160, 160, 80, 110, 110];
    // minimum width (any leftover space is split evenly between them).
    const FLEX_BASE = 110;
    const fillColgroup = (colgroup) => {
        COLUMN_WIDTHS.forEach(w => {
            const col = document.createElement('col');
            if (w) col.style.width = `${w}px`;
            colgroup.appendChild(col);
        });
    };
    fillColgroup(DOM.tableHeaderCols);
    fillColgroup(DOM.tableBodyCols);
    const minTableWidth = COLUMN_WIDTHS.reduce((sum, w) => sum + (w || FLEX_BASE), 0);
    document.querySelectorAll('.data-table').forEach(t => t.style.minWidth = `${minTableWidth}px`);

    const populateBooleanSelect = (selectElement) => {
        selectElement.innerHTML = '';
        selectElement.appendChild(new Option('Todo', '', true, true));
        selectElement.appendChild(new Option('Sí', '1'));
        selectElement.appendChild(new Option('No', '0'));
    };
    populateBooleanSelect(DOM.substituteFilter);
    populateBooleanSelect(DOM.electedFilter);

    // Year range inputs: restrict them to the years present in the data
    const minYear = Math.min(...years);
    const maxYear = Math.max(...years);
    DOM.yearMinFilter.min = minYear;
    DOM.yearMinFilter.max = maxYear;
    DOM.yearMaxFilter.min = minYear;
    DOM.yearMaxFilter.max = maxYear;

    const electionTypeValues = Array.from(electionTypes);
    DOM.electionTypeFilter.innerHTML = '';
    const defaultElectionOpt = new Option('Filtrar...', '');
    defaultElectionOpt.disabled = true;
    defaultElectionOpt.selected = true;
    defaultElectionOpt.hidden = true;
    DOM.electionTypeFilter.appendChild(defaultElectionOpt);
    electionTypeValues.sort((a, b) => prettifyElectionType(a).localeCompare(prettifyElectionType(b), 'es')).forEach(val => {
        DOM.electionTypeFilter.appendChild(new Option(prettifyElectionType(val), val));
    });
    // Populate all filters using the exact same logic
    populateSelect(DOM.provinceFilter, provinces);
    populateSelect(DOM.municipalityFilter, municipalities);

    // Initialize TomSelects
    tomSelects.electionType = new TomSelect(DOM.electionTypeFilter, tomSelectConfig);
    tomSelects.province = new TomSelect(DOM.provinceFilter, tomSelectConfig);
    tomSelects.municipality = new TomSelect(DOM.municipalityFilter, tomSelectConfig);

    // Update the text for the year range
    if (years.size > 1) {
        DOM.dataYearRangeText.textContent = ` (${minYear} - ${maxYear})`;
    } else if (years.size === 1) {
        DOM.dataYearRangeText.textContent = ` (${[...years][0]})`;
    }
}


function applyFilters() {
    const nameQuery = normalizeString(DOM.searchInput.value.trim());
    const nameTokens = nameQuery.split(/\s+/).filter(t => t.length > 0); 
    
    const partyQuery = normalizeString(DOM.partyInput.value.trim());
    const partyTokens = partyQuery.split(/\s+/).filter(t => t.length > 0);

    const selectedProv = tomSelects.province.getValue();
    const selectedMuni = tomSelects.municipality.getValue();
    let yearMin = parseInt(DOM.yearMinFilter.value, 10);
    const yearMax = parseInt(DOM.yearMaxFilter.value, 10);
    const selectedElection = tomSelects.electionType.getValue();
    const selectedSub = DOM.substituteFilter.value;
    const selectedElected = DOM.electedFilter.value;

    // If "Desde" > "Hasta" was typed, clamp it so the two inputs always
    // represent a valid range (the filter would otherwise yield 0 results)
    if (!isNaN(yearMin) && !isNaN(yearMax) && yearMin > yearMax) {
        DOM.yearMinFilter.value = yearMax;
        yearMin = yearMax;
    }

    filteredData = rawData.filter(row => {
        if (selectedProv && row.province !== selectedProv) return false;
        if (selectedMuni && row.municipality !== selectedMuni) return false;
        if (!isNaN(yearMin) && parseInt(row.year, 10) < yearMin) return false;
        if (!isNaN(yearMax) && parseInt(row.year, 10) > yearMax) return false;
        if (selectedElection && row.election_type !== selectedElection) return false;
        if (selectedSub && row.substitute !== selectedSub) return false;
        if (selectedElected && row.elected !== selectedElected) return false;

        if (nameTokens.length > 0) {
            const matchesAll = nameTokens.every(t => row._searchName.includes(t));
            if (!matchesAll) return false;
        }

        if (partyTokens.length > 0) {
            const matchesAll = partyTokens.every(t => row._partyFullNormalized.includes(t));
            if (!matchesAll) return false;
        }

        return true;
    });

    currentPage = 1;
    renderTable();
}


function renderTable() {
    DOM.tableBody.innerHTML = '';
    const totalItems = filteredData.length;
    const totalPages = Math.ceil(totalItems / rowsPerPage) || 1;
    
    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, totalItems);
    const pageData = filteredData.slice(startIndex, endIndex);

    const getBadge = (val, typeClass) => {
        if(val === "1" || val?.toLowerCase() === "sí" || val?.toLowerCase() === "si") {
            return `<span class="badge ${typeClass}">Sí</span>`;
        }
        return `<span class="badge badge-gray">No</span>`;
    };

    pageData.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = 'row-data';
        tr.innerHTML = `
            <td class="cell cell-name" title="${row.full_name || '-'}">${row.full_name || '-'}</td>
            <td class="cell cell-election-type">${prettifyElectionType(row.election_type)}</td>
            <td class="cell cell-year">${row.year}</td>
            <td class="cell cell-party" title="${row._partyFull}">${row._partyFull || '-'}</td>
            <td class="cell cell-province" title="${row.province || '-'}">${row.province || '-'}</td>
            <td class="cell cell-municipality" title="${row.municipality || '-'}">${row.municipality || '-'}</td>
            <td class="cell cell-order">${row.order || '-'}</td>
            <td class="cell cell-substitute">${getBadge(row.substitute, 'badge-yellow')}</td>
            <td class="cell cell-elected">${getBadge(row.elected, 'badge-green')}</td>
        `;
        DOM.tableBody.appendChild(tr);
    });

    DOM.resultsCount.innerText = `Mostrando ${totalItems.toLocaleString('es-ES')} resultados`;
    DOM.pageInput.value = currentPage;
    DOM.pageInput.max = totalPages;
    DOM.totalPagesText.innerText = `de ${totalPages}`;
    
    DOM.prevBtn.disabled = currentPage === 1;
    DOM.nextBtn.disabled = currentPage === totalPages || totalPages === 0;
}

function setupEventListeners() {
    let debounceTimer;
    
    const handleInputDebounce = () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(applyFilters, 300);
    };

    DOM.searchInput.addEventListener('input', handleInputDebounce);
    DOM.partyInput.addEventListener('input', handleInputDebounce);

    tomSelects.electionType.on('change', applyFilters);
    tomSelects.province.on('change', applyFilters);
    tomSelects.municipality.on('change', applyFilters);
    
    DOM.yearMinFilter.addEventListener('input', handleInputDebounce);
    DOM.yearMaxFilter.addEventListener('input', handleInputDebounce);

    // Clamp years typed outside the available range when the input loses focus
    ['yearMinFilter', 'yearMaxFilter'].forEach(id => {
        DOM[id].addEventListener('change', (e) => {
            let v = parseInt(e.target.value, 10);
            if (isNaN(v)) {
                e.target.value = '';
                return;
            }
            v = Math.max(parseInt(e.target.min, 10), Math.min(parseInt(e.target.max, 10), v));
            if (v !== e.target.value) e.target.value = v;
        });
    });
    DOM.electionTypeFilter.addEventListener('change', applyFilters);
    DOM.substituteFilter.addEventListener('change', applyFilters);
    DOM.electedFilter.addEventListener('change', applyFilters);

    // Keep the header strip (top scrollbar) and the body table horizontally
    // in sync, in both directions. The guard prevents re-entrance, because
    // assigning to scrollLeft fires the scroll event of the other wrapper.
    let isSyncingScroll = false;
    DOM.tableBodyScroll.addEventListener('scroll', () => {
        if (isSyncingScroll) return;
        isSyncingScroll = true;
        DOM.tableHeaderScroll.scrollLeft = DOM.tableBodyScroll.scrollLeft;
        isSyncingScroll = false;
    });
    DOM.tableHeaderScroll.addEventListener('scroll', () => {
        if (isSyncingScroll) return;
        isSyncingScroll = true;
        DOM.tableBodyScroll.scrollLeft = DOM.tableHeaderScroll.scrollLeft;
        isSyncingScroll = false;
    });

    DOM.prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    });

    DOM.nextBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(filteredData.length / rowsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    });

    DOM.pageInput.addEventListener('change', (e) => {
        const targetPage = parseInt(e.target.value, 10);
        const totalPages = Math.ceil(filteredData.length / rowsPerPage);
        if (targetPage >= 1 && targetPage <= totalPages) {
            currentPage = targetPage;
            renderTable();
        } else {
            DOM.pageInput.value = currentPage; 
        }
    });

    DOM.rowsPerPageSelect.addEventListener('change', (e) => {
        rowsPerPage = parseInt(e.target.value, 10);
        currentPage = 1;
        renderTable();
    });
}

document.addEventListener('DOMContentLoaded', loadData);
