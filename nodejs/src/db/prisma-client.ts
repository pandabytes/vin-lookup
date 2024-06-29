import { PrismaClient } from '@prisma/client'

// No need to explictly disconnect prisma as stated in
// https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections#prismaclient-in-long-running-applications
const prismaClient = new PrismaClient()

export default prismaClient
