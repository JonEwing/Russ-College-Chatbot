Sub Email_For_Unaswered_Queries()

' Code modified from orignal code by TeachExcel.

Dim emailApplication As Object
Dim emailItem As Object

Set emailApplication = CreateObject("Outlook.Application")
Set emailItem = emailApplication.CreateItem(0)

emailItem.to = "logan.s.gordon@gmail.com"

emailItem.Subject = "Weekly Unaswered Questions to Chatbot"

emailItem.Body = "The Unanswered Questions to the Russ Rufus Chatbot are in the Excel FIle attached. Please answer whatever questions you find pertinent and insert them into the Excel File for the Chatbot Database. Remember to run the Chatbot Database Formatter after updating the Chatbot Excel Database. Thank you for your Time."

emailItem.Attachments.Add ActiveWorkbook.FullName

' emailItem.Attachments.Add ("Excel file location goes here")

emailItem.Send

Set emailItem = Nothing
Set emailApplication = Nothing

End Sub
