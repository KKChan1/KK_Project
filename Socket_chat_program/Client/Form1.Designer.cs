namespace _06_Client
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
            btnStart = new Button();
            txtLog = new TextBox();
            txtMsg = new TextBox();
            btnSend = new Button();
            SuspendLayout();
            // 
            // txtServer
            // 
            txtServer.Location = new Point(129, 131);
            txtServer.Name = "txtServer";
            txtServer.Size = new Size(150, 30);
            txtServer.TabIndex = 12;
            txtServer.Text = "192.168.3.122";
            // 
            // txtPort
            // 
            txtPort.Location = new Point(318, 131);
            txtPort.Name = "txtPort";
            txtPort.Size = new Size(58, 30);
            txtPort.TabIndex = 13;
            txtPort.Text = "50000";
            // 
            // btnStart
            // 
            btnStart.Location = new Point(489, 127);
            btnStart.Name = "btnStart";
            btnStart.Size = new Size(112, 34);
            btnStart.TabIndex = 14;
            btnStart.Text = "連接";
            btnStart.UseVisualStyleBackColor = true;
            btnStart.Click += btnStart_Click;
            // 
            // txtLog
            // 
            txtLog.Location = new Point(129, 192);
            txtLog.Multiline = true;
            txtLog.Name = "txtLog";
            txtLog.Size = new Size(1098, 311);
            txtLog.TabIndex = 15;
            // 
            // txtMsg
            // 
            txtMsg.Location = new Point(129, 553);
            txtMsg.Multiline = true;
            txtMsg.Name = "txtMsg";
            txtMsg.Size = new Size(1098, 345);
            txtMsg.TabIndex = 16;
            // 
            // btnSend
            // 
            btnSend.Location = new Point(983, 950);
            btnSend.Name = "btnSend";
            btnSend.Size = new Size(112, 34);
            btnSend.TabIndex = 18;
            btnSend.Text = "發送消息";
            btnSend.UseVisualStyleBackColor = true;
            btnSend.Click += btnSend_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(11F, 23F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1472, 1121);
            Controls.Add(btnSend);
            Controls.Add(txtMsg);
            Controls.Add(txtLog);
            Controls.Add(btnStart);
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
        private Button btnStart;
        private TextBox txtLog;
        private TextBox txtMsg;
        private Button btnSend;
    }
}
