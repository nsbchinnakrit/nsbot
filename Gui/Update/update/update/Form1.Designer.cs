namespace update
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
            updatelabel = new Label();
            cancel_btn = new Button();
            process_label = new Label();
            progressBar = new ProgressBar();
            SuspendLayout();
            // 
            // updatelabel
            // 
            updatelabel.AutoSize = true;
            updatelabel.Font = new Font("Segoe UI", 9F, FontStyle.Regular, GraphicsUnit.Point);
            updatelabel.Location = new Point(14, 9);
            updatelabel.Name = "updatelabel";
            updatelabel.Size = new Size(92, 15);
            updatelabel.TabIndex = 1;
            updatelabel.Text = "Updating NSBot";
            // 
            // cancel_btn
            // 
            cancel_btn.Location = new Point(306, 57);
            cancel_btn.Name = "cancel_btn";
            cancel_btn.Size = new Size(74, 23);
            cancel_btn.TabIndex = 2;
            cancel_btn.Text = "Cancel";
            cancel_btn.UseVisualStyleBackColor = true;
            cancel_btn.Click += cancel_btn_Click;
            // 
            // process_label
            // 
            process_label.AutoSize = true;
            process_label.Location = new Point(14, 65);
            process_label.Name = "process_label";
            process_label.Size = new Size(93, 15);
            process_label.TabIndex = 3;
            process_label.Text = "Getting Version..";
            // 
            // progressBar
            // 
            progressBar.Location = new Point(17, 30);
            progressBar.Name = "progressBar";
            progressBar.Size = new Size(363, 18);
            progressBar.TabIndex = 0;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(397, 87);
            Controls.Add(process_label);
            Controls.Add(cancel_btn);
            Controls.Add(updatelabel);
            Controls.Add(progressBar);
            MaximizeBox = false;
            Name = "Form1";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "NSBot";
            Load += Form1_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        //private ProgressBar progressBar;
        private Label updatelabel;
        private Button cancel_btn;
        private Label process_label;
        private ProgressBar progressBar;
    }
}