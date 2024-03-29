document.addEventListener('DOMContentLoaded', function() {
  
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email={}) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // If email is a response
  if (email != {}){
    if (email.sender.length > 0){
      document.querySelector('#compose-recipients').value = email.sender;
      if (email.subject.slice(0, 3).toUpperCase() === "Re:".toUpperCase()){
        document.querySelector('#compose-subject').value = `${email.subject}`;
      } else {
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      }
      
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
    }
  } 

  //Get fields on submit
  document.querySelector("form").onsubmit = function(){
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    
    // send email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {

      if (result.message === "Email sent successfully.") {
        // Show succes message
        show_alert(result.message, 'success', '#compose-view');

        // Clear out Fields
        document.querySelector('#compose-recipients').value = '';
        document.querySelector('#compose-subject').value = '';
        document.querySelector('#compose-body').value = '';
      } else {
        console.log(result);
        // Show error message
        show_alert(result.error, 'danger', '#compose-view');
      }
    });
    // Stop page reload
    return false;
  };

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show inbox
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach((email)=>{
      // Create element
      const div = document.createElement("div");
      if (email.read){
        // Read
        div.className = 'list-group-item list-group-item-secondary'
      } else {
        // Unread
        div.className = 'list-group-item list-group-item-light'
      }

      // Text to show
      div.innerHTML = `<b>${email.sender}</b>  ${email.subject} <span class="text-right badge badge-primary badge-pill">${email.timestamp}</span>`;

      // Add EvenListener
      div.addEventListener('click',function(){
        // Show email if user clics
        show_email(email, mailbox);

      });
      document.querySelector('#emails-view').appendChild(div);

    });
    

  });
}

function show_email(email, mailbox) {

  // Hide other Views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  // Clear old emails
  document.querySelector('#email-view').innerHTML = '';

  // Mark email as read
  fetch(`emails/${email.id}`,{
    method: 'PUT',
    body:JSON.stringify({
      read:true
    })
  });

  //Update local status
  email.read = true;

  // Archive 
  const archive_button = document.createElement('button')
  if (email.archived) {
    archive_button.className = "btn btn-info";
    archive_button.innerHTML = "Unarchive";
  } else {
    archive_button.className = "btn btn-dark";
    archive_button.innerHTML = "Archive";
  }
  // Event listener for achive/unachive
  archive_button.addEventListener('click',function(){

    fetch(`emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !email.archived
      })
    });

    // Show alert and change style onclick
    if (!email.archived) {
      show_alert('Email Archive correctly', 'success', '#email-view');
      archive_button.className = "btn btn-info";
      archive_button.innerHTML = "Unarchive";
    } else {
      show_alert('Email Unarchive correctly', 'success', '#email-view');
      archive_button.className = "btn btn-dark";
      archive_button.innerHTML = "Archive";
    }
    // Update local status
    email.archived = !email.archived;
  });

  //Reply
  const reply_button = document.createElement('button');
  reply_button.className = "btn btn-primary";
  reply_button.innerHTML = "Reply"
  reply_button.addEventListener('click',function(){
    compose_email(email);
  })
  
  // Clean this
  console.log(email);
  let div = document.createElement("div");
  div.innerHTML = `<b>From:</b> ${email.sender}`;
  document.querySelector('#email-view').appendChild(div);
  div = document.createElement("div");
  div.innerHTML = `<b>To:</b> ${email.recipients}`;
  document.querySelector('#email-view').appendChild(div);
  div = document.createElement("div");
  div.innerHTML = `<b>Subject:</b> ${email.subject}`;
  document.querySelector('#email-view').appendChild(div);
  div = document.createElement("div");
  div.innerHTML = `<b>Timestamp:</b> ${email.timestamp}`;
  document.querySelector('#email-view').appendChild(div);
  div = document.createElement("div");
  if (mailbox !== "sent"){
    document.querySelector('#email-view').appendChild(archive_button);
    document.querySelector('#email-view').appendChild(reply_button);
  }
  div.innerHTML = `<hr>${email.body}`;
  document.querySelector('#email-view').appendChild(div);

}


function show_alert(text, alert_class, alert_location) {
  // Clear out old allerts
  document.querySelectorAll('.alert').forEach(alert => alert.remove());

  // Create new alert
  const div = document.createElement("div");
  div.className = `alert alert-${alert_class}`;
  div.innerHTML = text;
  document.querySelector(`${alert_location}`).prepend(div);
}

function reply_email(email) {

}