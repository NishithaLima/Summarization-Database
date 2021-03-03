import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSelectChange } from '@angular/material/select';
import spoken from "../../assets/spoken.js";

@Component({
  selector: 'app-summarize-queries',
  templateUrl: './summarize-queries.component.html',
  styleUrls: ['./summarize-queries.component.css']
})
export class SummarizeQueriesComponent implements OnInit {

  constructor(private http: HttpClient) { }

  tables: string[];
  contentTypes: string[] = ['Rows', 'Columns', 'Headers']
  listeningText: string;
  selectedTable: string;
  selectedQueryType: string;

  columnNames: string[];
  rowsData: string[];

  table_flag: boolean;
  continue_flag: boolean;
  summary_flag: boolean;

  ngOnInit(): void {
    this.getTableData();
    this.table_flag = false;
    this.continue_flag = false;
    this.summary_flag = false;

    spoken.say('Hello, Select table from dropdown to summarize').then(speech => {
      // spoken.listen().then(transcript => {
      //   console.log("Answer: " + transcript);
      //   this.listeningText = transcript;
      // })
    });

    var createNewString = function (oldStringObj, string) {
      var _new = new String(string);

      var keys = Object.keys(oldStringObj);  // returns only custom properties (not part of prototype)
      for (var i = 0, n = keys.length; i < n; i++) {
        var key = keys[i];

        if (Number.isInteger(+key)) {
          continue;                         // skip property if it's a numbered key
        }
        _new[key] = oldStringObj[key];       // simple assignment (not a deep copy) -- room for improvement
      }
      return _new;
    };

    // Setup Listener Events
    spoken.listen.on.partial(transcript => {
      transcript = transcript.toLowerCase(); 
      if (this.continue_flag) {
        if (transcript.includes("row") || transcript.includes("bro") ||transcript.includes("roar")){ 
          spoken.say("Here would be you row summary")
          this.stopCapture()
          this.resetFlags()
        }
        else if (transcript.includes("column")){
          spoken.say("Here would be you column summary")
          this.stopCapture()
          this.resetFlags()

        }
        else if (transcript.includes("table")){
          spoken.say("Here would be you table summary")
          this.stopCapture()
          this.resetFlags()

        }
      }



      else if (this.table_flag) {
        if (transcript.includes("yes") || transcript.includes("okay") ||transcript.includes("sure") || transcript.includes("yeah") || transcript.includes("ya")) {
          this.continue_flag = true;
          
          spoken.say('would you like row, column or table summary?')



        }
        else if (transcript.includes("no") || transcript.includes("nope") ||
          transcript.includes("end")){ 
          this.stopCapture();
            
          console.log("Ending Analysis: " + transcript);
          spoken.say('okay. Please change the selected table to start analysis on a table')

          
        }

      }
    
    });

    spoken.listen.on.end(this.continueCapture);
    spoken.listen.on.error(this.continueCapture);

  }

  resetFlags() {
    this.table_flag = false;
    this.continue_flag = false;
    this.summary_flag = false;
  }

  startCapture() {
    spoken.listen({ continuous: true }).then(transcript =>
      console.log('Started Listening')
    ).catch(e => true);
  }

  async continueCapture() {
    await spoken.delay(1);
    spoken.listen.stop();
    console.log('Stopped Listening');
    if (spoken.recognition.continuous) this.startCapture();
  }

  stopCapture() {
    spoken.recognition.continuous = false;
    spoken.listen.stop();
  }

  getTableData() {
    // this.http.get('http://localhost:5000/tables').subscribe(data => {
    this.http.get('http://127.0.0.1:5000/table_min_row?min=500').subscribe(data => {
      console.log(data);
      this.tables = data['tables'];
    });
  }


  selectedValue(event: MatSelectChange) {
    this.selectedTable = event.value;
    this.table_flag = false;
    if (this.selectedTable) {
      this.table_flag = true;
      var tbl_name = this.selectedTable.replaceAll("_", " ")
      console.log(tbl_name);
      

      this.http.get('http://127.0.0.1:5000/table_row_col_count?tbl='+this.selectedTable).subscribe(data => {
        console.log(data);
        // debugger;
        var str = 'You have selected table ' + tbl_name + '. This table has ' + data['rows'] + ' rows and ' + data['cols'] + ' columns. Would you like to analyze further?'
        spoken.say(str).then(speech => {});
        
        this.startCapture();
      });

      this.http.get('http://127.0.0.1:5000/tablesData?tbl='+this.selectedTable).subscribe(data => {
        let tableData = data['tables'];
        this.columnNames = tableData?.columnNames;
        this.rowsData = tableData?.rowsData;
        console.log(data);
      });
    }
  }


  

  selectedQueryValue(event: MatSelectChange) {
    this.selectedQueryType = event.value;
    console.log(event.value);
  }

  getSummarizedOutput(event) {
    
    let data = "You have selected " + this.selectedTable + "and query type" + this.selectedQueryType;
    if (this.selectedTable) {
      // Call the endpoint and assign it to spoken ( this.http.get(url).subscribe(data))
    } else {
      data = "Please select any table from dropdown to summarize";
    }

    spoken.say(data).then (transcript =>
      console.log('Started Listening'),
      this.listeningText = data,
    ).catch(e => true);
  }

}
