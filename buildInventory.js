var AWS = require('aws-sdk');
var fs = require("fs");

AWS.config.loadFromPath("./awsConfig.json");
var hostsPath = "./hosts";
try {
    console.log("Deleting existing 'hosts' file.")
    fs.unlinkSync(hostsPath);
} 
catch (e) {
    console.log("No 'hosts' file exists.");
}

var ec2 = new AWS.EC2();

var ec2Instance = JSON.parse(fs.readFileSync("ec2.json", "utf8"));

var params = {
    InstanceIds: [ec2Instance.InstanceId]
};


ec2.describeInstances(params, function(error, data) {
    if (error) {
        console.log(error); // an error occurred
    } else {
        var ec2IP = data.Reservations[0].Instances[0].NetworkInterfaces[0].Association.PublicIp;
        var ec2Host = "[awsEc2]\n" + ec2IP + " ansible_ssh_user=ubuntu ansible_ssh_private_key_file=/Users/dana/.ssh/mac_aws.pem\n\n";
        fs.appendFile(hostsPath, ec2Host, function(err) {
            if(err) {
                console.log("Error saving ec2 ip to file, err: " + err);
            }

            console.log("Appended ec2 host");
        });
    }
});
