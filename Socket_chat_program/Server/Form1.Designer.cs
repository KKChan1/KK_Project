namespace _06_Server
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            txtServer = new TextBox();
            txtPort = new TextBox();
            button1 = new Button();
            txtLog = new TextBox();
            txtMsg = new TextBox();
            txtPath = new TextBox();
            btnSelect = new Button();
            btnSendFile = new Button();
            btnSend = new Button();
            btnZD = new Button();
            cboUsers = new ComboBox();
            SuspendLayout();
            // 
            // txtServer
            // 
            txtServer.Location = new Point(113, 146);
            txtServer.Name = "txtServer";
            txtServer.Size = new Size(150, 30);
            txtServer.TabIndex = 0;
            txtServer.Text = "192.168.1.148";
            // 
            // txtPort
            // 
            txtPort.Location = new Point(302, 146);
            txtPort.Name = "txtPort";
            txtPort.Size = new Size(58, 30);
            txtPort.TabIndex = 1;
            txtPort.Text = "50000";
            // 
            // button1
            // 
            button1.Location = new Point(647, 146);
            button1.Name = "button1";
            button1.Size = new Size(112, 34);
            button1.TabIndex = 2;
            button1.Text = "開始監聽";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // txtLog
            // 
            txtLog.Location = new Point(113, 207);
            txtLog.Multiline = true;
            txtLog.Name = "txtLog";
            txtLog.Size = new Size(1098, 311);
            txtLog.TabIndex = 3;
            // 
            // txtMsg
            // 
            txtMsg.Location = new Point(113, 568);
            txtMsg.Multiline = true;
            txtMsg.Name = "txtMsg";
            txtMsg.Size = new Size(1098, 345);
            txtMsg.TabIndex = 4;
            // 
            // txtPath
            // 
            txtPath.Location = new Point(113, 963);
            txtPath.Name = "txtPath";
            txtPath.Size = new Size(863, 30);
            txtPath.TabIndex = 5;
            // 
            // btnSelect
            // 
            btnSelect.Location = new Point(1054, 970);
            btnSelect.Name = "btnSelect";
            btnSelect.Size = new Size(112, 34);
            btnSelect.TabIndex = 7;
            btnSelect.Text = "選擇";
            btnSelect.UseVisualStyleBackColor = true;
            btnSelect.Click += btnSelect_Click;
            // 
            // btnSendFile
            // 
            btnSendFile.Location = new Point(1216, 970);
            btnSendFile.Name = "btnSendFile";
            btnSendFile.Size = new Size(112, 34);
            btnSendFile.TabIndex = 8;
            btnSendFile.Text = "發送文件";
            btnSendFile.UseVisualStyleBackColor = true;
            btnSendFile.Click += btnSendFile_Click;
            // 
            // btnSend
            // 
            btnSend.Location = new Point(947, 1044);
            btnSend.Name = "btnSend";
            btnSend.Size = new Size(112, 34);
            btnSend.TabIndex = 9;
            btnSend.Text = "發送信息";
            btnSend.UseVisualStyleBackColor = true;
            btnSend.Click += btnSend_Click;
            // 
            // btnZD
            // 
            btnZD.Location = new Point(1131, 1044);
            btnZD.Name = "btnZD";
            btnZD.Size = new Size(112, 34);
            btnZD.TabIndex = 10;
            btnZD.Text = "震動";
            btnZD.UseVisualStyleBackColor = true;
            btnZD.Click += btnZD_Click;
            // 
            // cboUsers
            // 
            cboUsers.FormattingEnabled = true;
            cboUsers.Location = new Point(794, 149);
            cboUsers.Name = "cboUsers";
            cboUsers.Size = new Size(315, 31);
            cboUsers.TabIndex = 11;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(11F, 23F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1439, 1139);
            Controls.Add(cboUsers);
            Controls.Add(btnZD);
            Controls.Add(btnSend);
            Controls.Add(btnSendFile);
            Controls.Add(btnSelect);
            Controls.Add(txtPath);
            Controls.Add(txtMsg);
            Controls.Add(txtLog);
            Controls.Add(button1);
            Controls.Add(txtPort);
            Controls.Add(txtServer);
            Name = "Form1";
            Text = "Form1";
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox txtServer;
        private TextBox txtPort;
        private Button button1;
        private TextBox txtLog;
        private TextBox txtMsg;
        private TextBox txtPath;
        private Button btnSelect;
        private Button btnSendFile;
        private Button btnSend;
        private Button btnZD;
        private ComboBox cboUsers;
    }
}
