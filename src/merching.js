// TODO: I'm trying to get table_data to be modifiable anywhere in here. I may need to make an object for this.
var table_data = {}

window.addEventListener('pywebviewready', function() {
    FetchData()
    window.setTimeout(FetchData, 300000)
})

function FetchData(){
    pywebview.api.FetchData().then(SaveTableData, ShowErrorMessage)
    InsertTable()
}

function SaveTableData(response) {
    //table_data = response
    window.table_data = {"error": "Hi from error"}
}

function ShowErrorMessage(response) {
    window.table_data = {"error": response}
}

function InsertTable() {
    console.log(window.table_data)
    var merching_table = document.getElementById('merching-table')

    let error = "error" in window.table_data
    if(error) {
        merching_table.innerHTML = window.table_data["error"]
    }
    console.log(error)
}

function Initialize() {
    // pywebview.api.init().then(showResponse)
}


