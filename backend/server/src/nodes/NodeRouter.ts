import express, { Request, Response, Router } from "express";
import { MongoClient } from "mongodb";
import {
  IServiceResponse,
  failureServiceResponse,
  successfulServiceResponse,
  IImage,
} from "../types";

export const NodeExpressRouter = express.Router();

/**
 * NodeRouter uses NodeExpressRouter (an express router) to define responses
 * for specific HTTP requests at routes starting with '/node'.
 * E.g. a post request to '/node/create' would create a node.
 * The NodeRouter contains a BackendNodeGateway so that when an HTTP request
 * is received, the NodeRouter can call specific methods on BackendNodeGateway
 * to trigger the appropriate response. See server/src/app.ts to see how
 * we set up NodeRouter - you don't need to know the details of this just yet.
 */
export class NodeRouter {
  client: MongoClient;
  collectionName: string;

  constructor(mongoClient: MongoClient, collectionName?: string) {
    this.client = mongoClient;
    this.collectionName = collectionName ?? "product";

    /**
     * Request to retrieve image from database
     *
     * @param req request object coming from client
     * @param res response object to send to client
     */
    NodeExpressRouter.get("/getImage", async (req: Request, res: Response) => {
      try {
        let response: IServiceResponse<IImage>;
        const findResponse = await this.client
          .db()
          .collection(this.collectionName)
          .findOne({});
        if (findResponse == null) {
          response = failureServiceResponse(
            "Failed to get image from database."
          );
        } else {
          response = successfulServiceResponse(findResponse);
        }
        res.status(200).send(response);
      } catch (e) {
        res.status(500).send(e.message);
      }
    });

    /**
     * Request to insert image into database
     *
     * @param req request object coming from client
     * @param res response object to send to client
     */
    NodeExpressRouter.post("/create", async (req: Request, res: Response) => {
      try {
        let response: IServiceResponse<IImage>;
        const image: IImage = {
          path: req.body.path,
          description: req.body.description,
        };
        const addResponse = await this.client
          .db()
          .collection(this.collectionName)
          .insertOne(image);
        if (addResponse.insertedCount) {
          response = successfulServiceResponse(addResponse.ops[0]);
        } else {
          response = failureServiceResponse(
            "Failed to insert image, insertCount: " + addResponse.insertedCount
          );
        }
        res.status(200).send(response);
      } catch (e) {
        res.status(500).send(e.message);
      }
    });
  }

  /**
   * @returns NodeRouter class
   */
  getExpressRouter = (): Router => {
    return NodeExpressRouter;
  };
}
