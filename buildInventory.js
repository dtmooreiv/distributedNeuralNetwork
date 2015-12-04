var AWS = require('aws-sdk');
var fs = require("fs");

AWS.config.loadFromPath("./awsConfig.json");
var hostsPath = "./hosts";
var slavePath = "./slaves";

try {
    console.log("Deleting existing 'hosts' file.");
    fs.unlinkSync(hostsPath);
    console.log("Deleting existing 'slaves' file.");
    fs.unlinkSync(slavePath);
} 
catch (e) {
    console.log("No 'hosts' or 'slaves' file exists.");
}

var ec2 = new AWS.EC2();

var ec2Instances = JSON.parse(fs.readFileSync("ec2.json", "utf8"));

var instanceIds = []

for(i in ec2Instances) {
    instanceIds.push(ec2Instances[i].InstanceId);
}

var params = {
    InstanceIds: instanceIds
};


ec2.describeInstances(params, function(error, data) {
    if (error) {
        console.log(error); // an error occurred
    } else {
        fs.appendFileSync(hostsPath, "[awsEc2]\n");

        fs.appendFileSync(slavePath, "[slaves]\n");

        for(i in data.Reservations[0].Instances) {
            var ec2IP = data.Reservations[0].Instances[i].NetworkInterfaces[0].Association.PublicIp;
            var ec2Host = ec2IP + " ansible_ssh_user=ubuntu ansible_ssh_private_key_file=/Users/dana/.ssh/mac_aws_west.pem\n";
            fs.appendFileSync(hostsPath, ec2Host);

            if(i > 0) {
                fs.appendFileSync(slavePath, ec2Host);
            }
        }
    }
});
