# Things Terraform should tell us when it is finished

output "DB_URL" {
  value = aws_db_instance.games-tracker-db.address
}