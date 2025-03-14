package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/v2/contractapi"
)

// SmartContract provides functions for managing an Asset
type SmartContract struct {
	contractapi.Contract
}

// Asset describes basic details of what makes up a simple asset
// Insert struct field in alphabetic order => to achieve determinism across languages
// golang keeps the order when marshal to json but doesn't order automatically
type Asset struct {
	CertificateId string `json:"CertificateId"`
	CourseID      string `json:"CourseID"`
	Owner         string `json:"Owner"`
}

// InitLedger adds a base set of assets to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	assets := []Asset{
		{CertificateId: "1", CourseID: "5", Owner: "Tomoko"},
		{CertificateId: "2", CourseID: "5", Owner: "Brad"},
		{CertificateId: "3", CourseID: "10", Owner: "Jin Soo"},
		{CertificateId: "4", CourseID: "10", Owner: "Max"},
		{CertificateId: "5", CourseID: "15", Owner: "Adriana"},
		{CertificateId: "6", CourseID: "15", Owner: "Michel"},
	}

	for _, asset := range assets {
		assetJSON, err := json.Marshal(asset)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(asset.CertificateId, assetJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state. %v", err)
		}
	}

	return nil
}

// CreateAsset issues a new asset to the world state with given details.
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface, certificateid string, courseid string, owner string) error {
	exists, err := s.AssetExists(ctx, certificateid)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", certificateid)
	}

	asset := Asset{
		CertificateId: certificateid,
		CourseID:      courseid,
		Owner:         owner,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(certificateid, assetJSON)
}

// ReadAsset returns the asset stored in the world state with given certificateid.
func (s *SmartContract) ReadAsset(ctx contractapi.TransactionContextInterface, certificateid string) (*Asset, error) {
	assetJSON, err := ctx.GetStub().GetState(certificateid)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", certificateid)
	}

	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// UpdateAsset updates an existing asset in the world state with provided parameters.
func (s *SmartContract) UpdateAsset(ctx contractapi.TransactionContextInterface, certificateid string, courseid string, owner string) error {
	exists, err := s.AssetExists(ctx, certificateid)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", certificateid)
	}

	// overwriting original asset with new asset
	asset := Asset{
		CertificateId: certificateid,
		CourseID:      courseid,
		Owner:         owner,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(certificateid, assetJSON)
}

// DeleteAsset deletes an given asset from the world state.
func (s *SmartContract) DeleteAsset(ctx contractapi.TransactionContextInterface, certificateid string) error {
	exists, err := s.AssetExists(ctx, certificateid)
	if err != nil {
		return err
	}
	if !exists {
		return fmt.Errorf("the asset %s does not exist", certificateid)
	}

	return ctx.GetStub().DelState(certificateid)
}

// AssetExists returns true when asset with given certificateid exists in world state
func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, certificateid string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(certificateid)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

// TransferAsset updates the owner field of asset with given certificateid in world state, and returns the old owner.
func (s *SmartContract) TransferAsset(ctx contractapi.TransactionContextInterface, certificateid string, newOwner string) (string, error) {
	asset, err := s.ReadAsset(ctx, certificateid)
	if err != nil {
		return "", err
	}

	oldOwner := asset.Owner
	asset.Owner = newOwner

	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return "", err
	}

	err = ctx.GetStub().PutState(certificateid, assetJSON)
	if err != nil {
		return "", err
	}

	return oldOwner, nil
}

// GetAllAssets returns all assets found in world state
func (s *SmartContract) GetAllAssets(ctx contractapi.TransactionContextInterface) ([]*Asset, error) {
	// range query with empty string for startKey and endKey does an
	// open-ended query of all assets in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Asset
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Asset
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}
